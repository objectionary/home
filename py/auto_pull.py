# SPDX-FileCopyrightText: Copyright (c) 2016-2025 Objectionary.com
# SPDX-License-Identifier: MIT

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
            pull_exit_code = os.system(f'./pull.sh objectionary/{name}')
            if pull_exit_code != 0:
                raise RuntimeError(f"Failed to pull objectionary/{name}, exit code: {pull_exit_code}")
            pom_exit_code = os.system(f'./pom.sh {latest_version}')
            if pom_exit_code != 0:
                raise RuntimeError(f"Failed to update pom with version {latest_version}, exit code: {pom_exit_code}")
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
