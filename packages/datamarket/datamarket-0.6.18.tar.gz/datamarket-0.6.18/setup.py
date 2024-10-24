"""
Project setup module.
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = [
    "sqlalchemy",
    "clickhouse-driver",
    "requests[socks]",
    "tenacity",
    "stem",
    "pydrive2",
    "undetected-chromedriver",
    "pendulum",
    "boto3",
    "inflection",
]

setuptools.setup(
    name="datamarket",
    version="0.6.18",
    author="DataMarket",
    author_email="techsupport@datamarket.es",
    description="Utilities that integrate advance scraping knowledge into just one library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Data-Market/datamarket",
    project_urls={
        "Website": "https://datamarket.es",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=requirements,
)
