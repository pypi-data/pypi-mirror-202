from dataclasses import dataclass
import datetime
import json
import logging
import time

import requests
import yaml


@dataclass
class CommonOption:
    admin_url: str
    output: str = "json"
    indent: int = 4


class AdminClient(object):
    def __init__(self, common_option: CommonOption):
        self._common_option = common_option
        self._admin_url = self._common_option.admin_url
        self._output = self._common_option.output
        self._indent = self._common_option.indent

    def _extract_namespace(self, cluster):
        settings = json.loads(cluster.get("settings", None) or {})
        namespace = settings.get("namespace", None) or None

        changed_name = cluster["name"].replace("_", "-")

        namespace = namespace or changed_name

        return namespace

    def _parse_proxy_service(self, yamls_str):
        find = False
        proxy_name = None

        for each in yaml.load_all(yamls_str, Loader=yaml.Loader):
            if find:
                break

            if not isinstance(each, dict):
                continue

            kind = each.get("kind", "")
            if kind == "Service":
                port_list = each["spec"]["ports"]
                for port_spec in port_list:
                    if port_spec["port"] == 8088:
                        find = True
                        proxy_name = each["metadata"]["name"]

        return proxy_name

    def _send_delete(self, url):
        response = requests.delete(self._admin_url + url)

        if response.ok:
            return True
        else:
            return False

    def _send_get(self, url, params=None):
        params = params or {}
        response = requests.get(self._admin_url + url, params=params)

        if response.ok:
            return response.json() if response.text else None
        else:
            raise requests.exceptions.HTTPError(response.status_code)

    def _send_post(self, url, json_data: dict = None):
        json_data = json_data or {}
        response = requests.post(self._admin_url + url, json=json_data)

        if response.ok:
            return response.json() if response.text else None
        else:
            raise requests.exceptions.HTTPError(response.status_code)

    def _yaml_load_all(self, filepath):
        yamls = []

        for each in yaml.load_all(open(filepath, "r"), Loader=yaml.Loader):
            yamls.append(each)

        return yamls

    def print(self, dictionary):
        dictionary = dictionary or {}
        if self._output == "json":
            print(json.dumps(dictionary, indent=self._indent))
        elif self._output == "yaml":
            print(yaml.dump(dictionary, indent=self._indent))


class Catalog(AdminClient):
    def __init__(self, common_option: CommonOption):
        super(Catalog, self).__init__(common_option)

    def delete(self, name: str = None, catalog_id: int = None):
        response = None
        catalog_identifier = catalog_id or name

        if catalog_id:
            response = self._send_delete(f"/v1/catalogs/{catalog_id}")
        elif name:
            catalogs = self._send_get("/v1/catalogs", params={"name": name})

            if catalogs:
                catalog = catalogs[0]

                catalog_id = catalog["id"]

                response = self._send_delete(f"/v1/catalogs/{catalog_id}")

        if response:
            logging.info(f"catalog id: {catalog_identifier} is successfully deleted!")
        else:
            logging.info(
                f"catalog id: {catalog_identifier} does not be successfully deleted!"
            )

        return response

    def list(self):
        catalogs = self._send_get("/v1/catalogs")

        self.print(catalogs)

    def ls(self):
        self.list()

    def get(self, name):
        catalogs = self._send_get("/v1/catalogs", {"name": name})

        if catalogs:
            catalog = catalogs[0]

            self.print(catalog)

    def rm(self, name: str = None, catalog_id: int = None):
        return self.delete(name, catalog_id)

    def submit(self, path):
        yamls = self._yaml_load_all(path)

        for each in yamls:
            version = each.get("version", None)
            action_type = each.get("type", None)

            if version in ["v1/catalog"]:
                catalog_config = each.get("catalog", None) or {}
                name = catalog_config.get("name", None)
                catalog_type = catalog_config.get("catalog_type", None)
                properties = catalog_config.get("properties", None)

                if not name:
                    print("invalid name", name)
                    break

                if not catalog_type:
                    print("invalid chart name", catalog_type)
                    break

                if action_type == "create":
                    response = self._send_post(
                        "/v1/catalogs",
                        json_data={
                            "name": name,
                            "catalog_type": catalog_type,
                            "properties": properties,
                        },
                    )

                    if response:
                        self.print(response)
                    else:
                        logging.warning("chart submit failed")
                elif action_type == "update":
                    catalog_id = catalog_config.get("id", None)

                    if catalog_id:
                        response = self._send_post(
                            f"/v1/catalogs/{catalog_id}",
                            json_data={
                                "name": name,
                                "catalog_type": catalog_type,
                                "properties": properties,
                            },
                        )

                        if response:
                            self.print(response)
                        else:
                            logging.warning("catalog submit failed")


class Cluster(AdminClient):
    def __init__(self, url):
        super(Cluster, self).__init__(url)

    def delete(self, name, force=False, refresh=1, timeout=120):
        clusters = self._send_get("/v1/clusters", {"name": name})

        if clusters:
            cluster = clusters[0]
            health_check = self._helath_check_status(cluster["id"])

            if health_check:
                if force:
                    self.off(name=name, refresh=refresh, timeout=timeout)
                else:
                    logging.warning("Cluster is on. please off the cluster first.")
                    return

            response = self._send_delete(f"/v1/clusters/{cluster['id']}")
            self.print(response)

    def _helath_check_status(self, cluster_id):
        health_check = None

        try:
            health_check = self._send_get(f"/v1/clusters/{cluster_id}/gateway/health")
        except Exception:
            pass

        if health_check:
            return True
        else:
            return False

    def _waiting_release(self, release_id, refresh, timeout):
        start_time = datetime.datetime.now(datetime.timezone.utc)

        response = self._send_get(f"/v1/releases/{release_id}")
        finished = False
        timeout_flag = False

        while response.get("status", "QUEUED") not in ["FINISHED", "FAILED"]:
            self.print(response)

            current_time = datetime.datetime.now(datetime.timezone.utc)

            if (current_time - start_time).seconds > timeout:
                timeout_flag = True
                break

            response = self._send_get(f"/v1/releases/{release_id}")
            self.print(response)
            time.sleep(refresh)

        if timeout_flag:
            finished = False
        else:
            finished = True

        return finished

    def _waiting_release_log(self, release_id, refresh, timeout):
        start_time = datetime.datetime.now(datetime.timezone.utc)

        response = self._send_get(f"/v1/releases/{release_id}/log")

        timeout_flag = False
        while response.get("state", "PENDING") not in ["SUCCESS", "FAILURE"]:
            current_time = datetime.datetime.now(datetime.timezone.utc)

            if (current_time - start_time).seconds > timeout:
                timeout_flag = True
                break

            response = self._send_get(f"/v1/releases/{release_id}/log")
            self.print(response)
            time.sleep(refresh)

        if timeout_flag:
            response = None

        return response

    def _do_install(self, cluster_id, refresh, timeout):
        install_response = self._send_post(f"/v1/clusters/{cluster_id}/install")

        release_id = install_response["id"]

        self.print(install_response)
        release_response = self._waiting_release(release_id, refresh, timeout)

        if not release_response:
            return None

        log_response = self._waiting_release_log(release_id, refresh, timeout)

        return log_response

    def _do_upgrade(self, cluster_id, refresh, timeout):
        upgarde_response = self._send_post(f"/v1/clusters/{cluster_id}/upgrade")

        release_id = upgarde_response["id"]

        self.print(upgarde_response)
        release_response = self._waiting_release(release_id, refresh, timeout)

        if not release_response:
            return None

        log_response = self._waiting_release_log(release_id, refresh, timeout)

        return log_response

    def list(self):
        clusters = self._send_get("/v1/clusters")

        for cluster in clusters:
            cluster["settings"] = json.loads(cluster["settings"])
            cluster["status"] = (
                "ON" if self._helath_check_status(cluster["id"]) else "OFF"
            )

        self.print(clusters)

    def ls(self):
        self.list()

    def get(self, name):
        clusters = self._send_get("/v1/clusters", {"name": name})

        if clusters:
            cluster = clusters[0]

            cluster["settings"] = json.loads(cluster["settings"])
            cluster["status"] = (
                "ON" if self._helath_check_status(cluster["id"]) else "OFF"
            )

            self.print(cluster)

    def status(self, name, refresh=1, timeout=120):
        cluster = None

        clusters = self._send_get("/v1/clusters", params={"name": name})
        if clusters:
            cluster = clusters[0]

        if not cluster:
            return

        cluster_response = self._send_get(f"/v1/clusters/{cluster['id']}/status")
        if not self._waiting_release(cluster_response["id"], refresh, timeout):
            # timeout
            return

        cluster_status_response = self._waiting_release_log(
            cluster_response["id"], refresh, timeout
        )

        response_log = cluster_status_response.get("log", {}) or {}
        return_value = response_log.get("return", {}) or {}

        is_cluster_installed = len(return_value.get("stdout", "")) > 0

        proxy_response = self._send_get(f"/v1/clusters/{cluster['id']}/proxy")
        if not self._waiting_release(proxy_response["id"], refresh, timeout):
            # timeout
            return

        proxy_status_response = self._waiting_release_log(
            proxy_response["id"], refresh, timeout
        )

        response_log = proxy_status_response.get("log", {}) or {}
        return_value = response_log.get("return", {}) or {}

        is_proxy_installed = len(return_value.get("stdout", "")) > 0

        status = {
            "cluster installed:": is_cluster_installed,
            "proxy installed:": is_proxy_installed,
            "cluster status (health check):": self._helath_check_status(cluster["id"]),
        }

        self.print(status)

    def rm(self, name, force=False, refresh=1, timeout=120):
        return self.delete(name, force, refresh, timeout)

    def submit(self, path):
        yamls = self._yaml_load_all(path)

        for each in yamls:
            version = each.get("version", None)
            action_type = each.get("type", None)

            if version in ["v1/cluster"]:
                cluster_config = each.get("cluster", None) or {}
                name = cluster_config.get("name", None)

                direct_on = cluster_config.get("direct_on", True)

                chart_name = cluster_config.get("chart", None)

                params = {"name": chart_name}

                charts = self._send_get("/v1/charts", params=params)

                if charts:
                    chart_id = charts[0]["id"]

                if not chart_id:
                    raise Exception("invalid chart options")

                catalog_config = cluster_config.get("catalogs", None) or []

                catalog_list = []

                for catalog_name in catalog_config:
                    response = self._send_get(f"/v1/catalogs?name={catalog_name}")

                    if response:
                        catalog_list.append(response[0]["id"])

                settings = cluster_config.get("settings", None) or {}

                if not name:
                    print("invalid name", name)
                    break

                if not chart_id:
                    print("invalid chart id or chart_name", chart_id, chart_name)
                    break

                if action_type == "create":
                    response = self._send_post(
                        "/v1/clusters",
                        json_data={
                            "name": name,
                            "chart_id": chart_id,
                            "catalog_list": catalog_list,
                            "settings": settings,
                        },
                    )

                    if response:
                        response["settings"] = json.loads(response["settings"])
                        self.print(response)
                        if direct_on:
                            self.on(cluster_id=response["id"], is_update=False)
                    else:
                        logging.warning("cluster submit failed")
                elif action_type == "update":
                    cluster_id = cluster_config.get("id", None)

                    if cluster_id:
                        response = self._send_post(
                            f"/v1/clusters/{cluster_id}",
                            json_data={
                                "name": name,
                                "chart_id": chart_id,
                                "catalog_list": catalog_list,
                                "settings": settings,
                            },
                        )

                        if response:
                            response["settings"] = json.loads(response["settings"])
                            self.print(response)
                            if direct_on:
                                self.on(cluster_id=cluster_id, is_update=True)
                        else:
                            logging.warning("cluster submit failed")
                    else:
                        logging.warning("cluster id is unknown.")

    def on(self, name=None, cluster_id=None, is_update=False, refresh=1, timeout=120):
        cluster = None
        cluster_identifer = name or cluster_id

        if cluster_id:
            cluster = self._send_get(f"/v1/clusters/{cluster_id}")
        if name:
            clusters = self._send_get("/v1/clusters", params={"name": name})

            if clusters:
                cluster = clusters[0]

        if not cluster:
            logging.warning(f"cluster: {cluster_identifer} is invalid")
            return

        cluster_id = cluster["id"]
        namespace_name = self._extract_namespace(cluster)

        response = {}

        if is_update:
            response = self._do_upgrade(cluster_id, refresh, timeout)
        else:
            response = self._do_install(cluster_id, refresh, timeout)

        response_log = response.get("log", {}) or {}
        return_value = response_log.get("return", {}) or {}

        if response_log.get("success", False) or False:
            logging.info(return_value)
            logging.info("cluster install is succeeded!")
            logging.info("try to register proxy to api gateway...")
        else:
            logging.warning(response_log)
            logging.warning("cluster install failed")
            return

        proxy_release = self._send_get(f"/v1/clusters/{cluster_id}/proxy/manifest")
        proxy_release_id = proxy_release["id"]

        proxy_manifest_ended = self._waiting_release(proxy_release_id, refresh, timeout)

        if not proxy_manifest_ended:
            logging.warning("getting cluster proxy information is failed")
            return None

        proxy_manifest = self._waiting_release_log(proxy_release_id, refresh, timeout)

        if not proxy_manifest:
            logging.warning("getting cluster proxy information is failed")
            return None

        response_log = proxy_manifest.get("log", {}) or {}
        return_value = response_log.get("return", {}) or {}

        if response_log.get("success", False) or False:
            pass
        else:
            logging.warning("get proxy info failed")
            return

        proxy_name = self._parse_proxy_service(return_value.get("stdout", ""))

        service_name = f"""{proxy_name}.{namespace_name}"""

        response = self._send_post(
            f"/v1/clusters/{cluster_id}/gateway/register",
            {"service_name": service_name},
        )

        logging.info(response)

    def off(self, name=None, cluster_id=None, refresh=1, timeout=120):
        cluster = None

        if cluster_id:
            cluster = self._send_get(f"/v1/clusters/{cluster_id}")
        if name:
            clusters = self._send_get("/v1/clusters", params={"name": name})

            if clusters:
                cluster = clusters[0]

        if not cluster:
            logging.warning("cluster id or name is invalid")
            return

        cluster_id = cluster["id"]

        response = self._send_delete(f"/v1/clusters/{cluster_id}/gateway/deregister")
        logging.info(response)

        response = self._send_post(f"/v1/clusters/{cluster_id}/uninstall")

        uninstall_response = self._waiting_release(response["id"], refresh, timeout)

        if not uninstall_response:
            logging.warning("cluster uninstall is failed")
        else:
            logging.info("cluster uninstall is succeeded!")


class HelmChart(AdminClient):
    def __init__(self, url):
        super(HelmChart, self).__init__(url)

    def delete(self, name: str = None, chart_id: int = None):
        response = None
        chart_identifier = chart_id or name

        if chart_id:
            response = self._send_delete(f"/v1/charts/{chart_id}")
        elif name:
            chart = self._send_get("/v1/charts", params={"name": name})

            if chart:
                chart_id = chart[0]["id"]

                response = self._send_delete(f"/v1/charts/{chart_id}")

        if response:
            logging.info(f"chart id: {chart_identifier} is successfully deleted!")
        else:
            logging.info(
                f"chart id: {chart_identifier} does not be successfully deleted!"
            )

        return response

    def get(self, name):
        charts = self._send_get("/v1/charts", {"name": name})

        if charts:
            chart = charts[0]
            chart["registry"] = json.loads(chart["registry"])
            chart["repository"] = json.loads(chart["repository"])

            self.print(charts)

    def list(self):
        helm_charts = self._send_get("/v1/charts")

        for chart in helm_charts:
            chart["registry"] = json.loads(chart["registry"])
            chart["repository"] = json.loads(chart["repository"])

        self.print(helm_charts)

    def ls(self):
        self.list()

    def rm(self, name: str = None, chart_id: int = None):
        return self.delete(name, chart_id)

    def submit(self, path):
        yamls = self._yaml_load_all(path)

        for each in yamls:
            version = each.get("version", None)
            action_type = each.get("type", None)

            if version in ["v1/chart"]:
                chart_config = each.get("chart", None) or {}
                name = chart_config.get("name", None)
                chart_name = chart_config.get("chart_name", None)
                chart_version = chart_config.get("version", None)
                registry = chart_config.get("registry", None) or {}
                repository = chart_config.get("repository", None) or {}

                if not name:
                    print("invalid name", name)
                    break

                if not chart_name:
                    print("invalid chart name", chart_name)
                    break

                if action_type == "create":
                    response = self._send_post(
                        "/v1/charts",
                        json_data={
                            "name": name,
                            "chart_name": chart_name,
                            "version": chart_version,
                            "registry": registry,
                            "repository": repository,
                        },
                    )

                    if response:
                        response["registry"] = json.loads(response["registry"])
                        response["repository"] = json.loads(response["repository"])
                        self.print(response)
                    else:
                        logging.warning("chart submit failed")
                elif action_type == "update":
                    chart_id = chart_config.get("id", None)

                    if chart_id:
                        response = self._send_post(
                            f"/v1/charts/{chart_id}",
                            json_data={
                                "name": name,
                                "chart_name": chart_name,
                                "version": chart_version,
                                "registry": registry,
                                "repository": repository,
                            },
                        )

                        if response:
                            response["registry"] = json.loads(response["registry"])
                            response["repository"] = json.loads(response["repository"])
                            self.print(response)
                        else:
                            logging.warning("chart submit failed")
