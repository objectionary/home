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
import subprocess
import sys

make_pr = False
if len(sys.argv) > 1:
    eo_lib_version = sys.argv[1]
    if eo_lib_version != '':
        print('cmd entry:', eo_lib_version)
        command = f'git ls-remote --exit-code --heads origin update-{eo_lib_version}'
        result = subprocess.run(command, shell=True, capture_output=True)
        make_pr = result.returncode != 0
else:
    print("eo_lib_version was not set to sys.argv")
env_file = os.getenv('GITHUB_ENV')
with open(env_file, "a") as file:
    env = f'make_pr={"true" if make_pr else "false"}'
    file.write(env)
    print(f'written to GITHUB_ENV "{env}"')
print(f'Added to env: {make_pr}')
