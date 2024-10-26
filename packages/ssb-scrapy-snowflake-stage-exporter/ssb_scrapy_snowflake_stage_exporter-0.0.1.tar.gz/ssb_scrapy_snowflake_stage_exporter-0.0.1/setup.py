from setuptools import find_packages, setup

setup(
    name="ssb-scrapy-snowflake-stage-exporter",
    version="0.0.1",
    description="Snowflake database exporting utility with Scrapy integration",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "itemadapter",
        "snowflake-connector-python",
    ],
)
