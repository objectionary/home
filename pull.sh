#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (c) 2016-2026 Objectionary.com
# SPDX-License-Identifier: MIT

set -e -o pipefail

# This script helps you create a pull request for Objectionary.
# When you have a directory with sources, which you are ready
# to push to Objectionary, make sure you have them in "gh-pages"
# branch in the "objectionary/" directory. You can see how it's
# organized in "objectionary/eo-files" repository.

repo=$1
if [ -z "${repo}" ]; then
    echo "One argument is required as a name of GitHub repository"
    echo "Read more here: https://github.com/objectionary/home"
    exit 1
fi

tmp=.tmp/${repo}

rm -rf "${tmp}"
git clone "https://github.com/${1}" --branch gh-pages --depth 1 --single-branch "${tmp}"
tree "${tmp}/objectionary"

# Objects that this library published before, but doesn't publish anymore,
# must disappear; objects of other libraries must stay untouched.
{ grep -rlZx --include='*.eo' -F "+home https://github.com/${repo}" objects || true; } \
    | xargs -0 rm -f
rsync -a "${tmp}/objectionary"/ objects/
find objects -type d -empty -delete

pdd --source objects --remove -f /dev/null
