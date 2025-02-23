#!/bin/bash
# SPDX-FileCopyrightText: Copyright (c) 2016-2025 Objectionary.com
# SPDX-License-Identifier: MIT

set -e

# This script updates version in pom.xml

# Check if the argument is provided
if [ $# -eq 0 ]; then
    echo "One argument is required as a new version to replace with in pom.xml"
    exit 1
fi

# Store the new version from the argument
new_version=$1

# Path to pom.xml file
pom_file="make/jvm/pom.xml"

# Replace the <eo.version> property with the new version
sed -i "s|<eo.version>.*</eo.version>|<eo.version>${new_version}</eo.version>|g" $pom_file

echo "Updated pom.xml with new version: ${new_version}"
