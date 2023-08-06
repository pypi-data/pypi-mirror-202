from setuptools import setup, find_packages


setup(
    name="tmctl",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["requests", "pyyaml", "fire"],
    description="TMCTL - Admin CLI for Trino Cluster Manager",
    entry_points={"console_scripts": "tmctl = tmctl:main"},
)
