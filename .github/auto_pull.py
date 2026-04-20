# SPDX-FileCopyrightText: Copyright (c) 2016-2026 Objectionary.com
# SPDX-License-Identifier: MIT

import os
import re
import requests


def dependencies():
    directory = "objects"
    unique_deps = set()
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".eo"):
                with open(os.path.join(subdir, file), "r") as f:
                    content = f.read()
                    matches = re.findall(r"\+rt jvm org.eolang:(.*?)\n", content)
                    for match in matches:
                        lst = match.split(":")
                        if len(lst) > 2:
                            match = f'{lst[0]}:{lst[2]}'
                        if "eo-runtime" in match:
                            match = f'eo:{lst[1]}'
                        unique_deps.add(match)
    print(f'List of current dependencies: {unique_deps}')
    return unique_deps


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
            pom_exit_code = os.system(f'./.github/pom.sh {latest_version}')
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
