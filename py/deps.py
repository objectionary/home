# The MIT License (MIT)
#
# Copyright (c) 2016-2024 Objectionary.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
