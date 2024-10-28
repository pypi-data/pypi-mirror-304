#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import setuptools

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name='webdriver_manager_zh',
    python_requires=">=3.7",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include=['webdriver_manager_zh*']),
    include_package_data=True,
    version='4.0.3',
    description='Library provides the way to automatically manage drivers for different browsers',
    url='https://github.com/SergeyPirogov/webdriver_manager',
    install_requires=[
        'requests',
        'python-dotenv',
        'packaging'
    ],
    package_data={
        "webdriver_manager_zh": ["py.typed"]
    },
)
