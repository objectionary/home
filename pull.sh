#!/bin/bash
set +x
set +e

repo=$1
tmp=$(mktemp -d)

git clone "https://github.com/${1}" --branch gh-pages --depth 1 --single-branch "${tmp}"
ls -al "${tmp}"
cp -r ${tmp}/objectionary/* .
