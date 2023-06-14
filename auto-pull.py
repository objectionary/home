import os
import requests

os.system(f'git checkout -b automated-release-update')

with open('releases.txt', 'r') as f:
    releases = f.readlines()

for release in releases:
    name, version = release.strip().split(':')
    url = f'https://api.github.com/repos/objectionary/{name}/releases/latest'
    response = requests.get(url)
    response.raise_for_status()
    latest_version = response.json()['tag_name']
    if latest_version > version:
        print(f'New release for {name}: {latest_version}')
        os.system(f'./pull.sh objectionary/{name}')
        with open('releases.txt', 'r') as f:
            data = f.read()
        data = data.replace(f'{name}:{version}', f'{name}:{latest_version}')
        with open('releases.txt', 'w') as f:
            f.write(data)
        os.system(f'git add .')
        os.system(f'git commit -m "Update {name} to {latest_version}"')