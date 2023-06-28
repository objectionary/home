import os
import re
import requests


def dependencies():
    directory = "objects/org/eolang"
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
        url = f'https://api.github.com/repos/objectionary/{name}/releases/latest'
        response = requests.get(url)
        response.raise_for_status()
        latest_version = response.json()['tag_name']
        if latest_version > version:
            os.system(f'./pull.sh objectionary/{name}')
            env_file = os.getenv('GITHUB_ENV')
            eo_lib_version = f'{name}_{latest_version}'
            with open(env_file, "a") as myfile:
                myfile.write(f'eo_lib_version={eo_lib_version}')
            print(f'Added to env: {eo_lib_version}')
            break


pull_release(dependencies())
