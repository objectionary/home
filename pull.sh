#!/bin/bash
set +x
set +e

# This script helps you create a pull request for Objectionary.
# When you have a directory with sources, which you are ready
# to push to Objectionary, make sure you have them in "gh-pages"
# branch in the "objectionary/" directory. You can see how it's
# organized in "objectionary/eo-files" repository.

repo=$1
tmp=$(mktemp -d)
trap 'rm -rf -- "${tmp}"' EXIT

git clone "https://github.com/${1}" --branch gh-pages --depth 1 --single-branch "${tmp}"
ls -al "${tmp}"
cp -r ${tmp}/objectionary/* .
