#!/bin/bash
# The MIT License (MIT)
#
# SPDX-FileCopyrightText: Copyright (c) 2016-2025 Objectionary.com
# SPDX-License-Identifier: MIT

set -e

# This script pulls all necessary components.

version=$1
if [ "${version}" == "" ]; then
	echo "One argument expected: the version of EO to upgrade to"
	exit 1
fi
if [[ ! "${version}" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
	echo "Wrong version: ${version}"
	exit 1
fi

git reset --hard
git clean -fd
rm -rf objects tests
make clean
rm -rf ~/.eo

sed -i "s|eo.version>[0-9]\+.[0-9]\+.[0-9]\+|eo.version>${version}|" make/jvm/pom.xml

./pull.sh objectionary/eo
