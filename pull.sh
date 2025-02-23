#!/bin/bash
# The MIT License (MIT)
#
# SPDX-FileCopyrightText: Copyright (c) 2016-2025 Objectionary.com
# SPDX-License-Identifier: MIT

set -e

# This script helps you create a pull request for Objectionary.
# When you have a directory with sources, which you are ready
# to push to Objectionary, make sure you have them in "gh-pages"
# branch in the "objectionary/" directory. You can see how it's
# organized in "objectionary/eo-files" repository.

repo=$1
if [ "${repo}" == "" ]; then
	echo "One argument is required as a name of GitHub repository"
	echo "Read more here: https://github.com/objectionary/home"
	exit 1
fi

set -x

tmp=$(mktemp -d)
trap 'rm -rf -- "${tmp}"' EXIT

git clone "https://github.com/${1}" --branch gh-pages --depth 1 --single-branch "${tmp}"
ls -al "${tmp}"
cp -r "${tmp}/objectionary/"/* .

pdd --remove -f /dev/null
