#!/usr/bin/env python

# Copyright 2023 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

"""The setup script."""

import json
import os
from setuptools import find_packages, find_namespace_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

with open(f"src{os.sep}taipy{os.sep}version.json") as version_file:
    version = json.load(version_file)
    version_string = f'{version.get("major", 0)}.{version.get("minor", 0)}.{version.get("patch", 0)}'
    if vext := version.get("ext"):
        version_string = f"{version_string}.{vext}"

requirements = [
    "taipy-gui>=2.2,<2.3",
    "taipy-rest>=2.2,<2.3",
]

test_requirements = ["pytest>=3.8"]

extras_require = {
    "ngrok": ["pyngrok>=5"],
    "image": ["python-magic;platform_system!='Windows'", "python-magic-bin;platform_system=='Windows'"],
    "rdp": ["rdp>=0.8"],
    "arrow": ["pyarrow>=7.0"],
    "mssql": ["pyodbc>=4"],
}

setup(
    author="Avaiga",
    author_email="dev@taipy.io",
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="The Python application builder. Turns Data and AI algorithms into full web apps in no time.",
    install_requires=requirements,
    license="Apache License 2.0",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords="taipy",
    name="taipy",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src") + find_packages(include=["taipy"]),
    include_package_data=True,
    test_suite="tests",
    url="https://github.com/avaiga/taipy",
    version=version_string,
    zip_safe=False,
    extras_require=extras_require,
)
