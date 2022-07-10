#!/bin/bash
# (The MIT License)
#
# Copyright (c) 2016-2021 Yegor Bugayenko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
