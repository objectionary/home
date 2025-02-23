# The MIT License (MIT)
#
# SPDX-FileCopyrightText: Copyright (c) 2016-2025 Objectionary.com
# SPDX-License-Identifier: MIT

import os
import re


def dependencies():
    directory = "objects/org/eolang"
    unique_deps = set()
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".eo"):
                with open(os.path.join(subdir, file), "r") as f:
                    content = f.read()
                    matches = re.findall(r"\+rt jvm org.eolang:(.*?)\n", content)
                    for match in matches:
                        lst = match.split(":")
                        if len(lst) > 2:
                            match = f'{lst[0]}:{lst[2]}'
                        if "eo-runtime" in match:
                            match = f'eo:{lst[1]}'
                        unique_deps.add(match)
    print(f'List of current dependencies: {unique_deps}')
    return unique_deps
