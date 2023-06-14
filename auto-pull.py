import os
import re
import requests

os.system(f'git checkout -b automated-release-update')

directory = "objects/org/eolang"
unique_deps = set()

# Recursively find all files in the directory
for subdir, dirs, files in os.walk(directory):
    for file in files:
        # Check if the file is a .eo file
        if file.endswith(".eo"):
            # Open the file and read its contents
            with open(os.path.join(subdir, file), "r") as f:
                content = f.read()
                # Find all dependencies in the file
                matches = re.findall(r"\+rt jvm org.eolang:(.*?)\n", content)
                # Add the dependencies to the set of unique dependencies
                for match in matches:
                    # Check if the dependency has the "jar-with-dependencies" suffix
                    lst = match.split(":")
                    if len(lst) > 2:
                        # Remove the suffix from the dependency string
                        match = f'{lst[0]}:{lst[2]}'
                    if "eo-runtime" in match:
                        match = f'eo:{lst[1]}'
                    unique_deps.add(match)

print(f'List of current dependencies: {unique_deps}')

# Iterate over the set of unique dependencies and extract the name and version
for dep in unique_deps:
    name, version = dep.split(":")
    print(f"{name} - {version}")
    url = f'https://api.github.com/repos/objectionary/{name}/releases/latest'
    response = requests.get(url)
    response.raise_for_status()
    latest_version = response.json()['tag_name']
    if latest_version > version:
        print(f'New release for {name}: {latest_version}')
        os.system(f'./pull.sh objectionary/{name}')
        os.system(f'git add .')
        os.system(f'git commit -m "Update {name} to {latest_version}"')