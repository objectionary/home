# The MIT License (MIT)
#
# Copyright (c) 2016-2025 Objectionary.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import requests
from deps import dependencies


def pull_release(unique_deps):
    for dep in unique_deps:
        name, version = dep.split(":")
        print(f"{name} - {version}")
        url = f'https://api.github.com/repos/objectionary/{name}/releases'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        latest_release = data[0]
        latest_version = latest_release["tag_name"]
        if compare(latest_version, version):
            os.system(f'./pull.sh objectionary/{name}')
            os.system(f'./pom.sh {latest_version}')
            env_file = os.getenv('GITHUB_ENV')
            eo_lib_version = f'{name}-{latest_version}'
            with open(env_file, "a") as myfile:
                myfile.write(f'eo_lib_version={eo_lib_version}')
            print(f'Added to env: {eo_lib_version}')
            break
        else:
            print(f"{latest_version} is less than or equal to {version}")


def compare(latest_version, old_version):
    latest = latest_version.split(".")
    old = old_version.split(".")
    for i in range(len(latest)):
        if int(latest[i]) > int(old[i]):
            return True
    return False


pull_release(dependencies())
