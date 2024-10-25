from pathlib import Path
from typing import Dict

from setuptools import find_packages, setup


def get_version() -> str:
    version: Dict[str, str] = {}
    with open(Path(__file__).parent / "dagster_cloud_examples/version.py", encoding="utf8") as fp:
        exec(fp.read(), version)

    return version["__version__"]


ver = get_version()
# dont pin dev installs to avoid pip dep resolver issues
pin = "" if ver == "1!0+dev" else f"=={ver}"
setup(
    name="dagster-cloud-examples",
    version=ver,
    packages=find_packages(exclude=["dagster_cloud_examples_tests*"]),
    install_requires=["dagster_cloud==1.8.13"],
    extras_require={"tests": ["mypy", "pylint", "pytest"]},
    author="Elementl",
    author_email="hello@elementl.com",
    license="Apache-2.0",
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
