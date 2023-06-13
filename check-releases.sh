#!/bin/bash

declare -A repos=(
  ["eo-strings"]="0.2.0"
  ["eo-collections"]="0.0.9"
)

for repo in "${!repos[@]}"; do
  latest_release=$(curl -s https://api.github.com/repos/objectionary/$repo/releases/latest | jq -r '.tag_name')

  if [[ "$(echo -e "${repos[$repo]}n$latest_release" | sort -V | tail -n 1)" = "$latest_release" ]]; then
    echo "Found new release for $repo: $latest_release"
    ./pull.sh "objectionary/$repo"
  else
    echo "There is no new releases in $repo"
  fi
done

