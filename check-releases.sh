#!/bin/bash

repositories=(
    "eo-strings"
    "eo-collections"
)

for repository in "${repositories[@]}"
do
    release=$(curl -s "https://api.github.com/repos/objectionary/$repository/releases/latest")
    version=$(echo "$release" | jq -r '.tag_name')
    echo "$repository latest release: $version"
done
