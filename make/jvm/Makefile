# SPDX-FileCopyrightText: Copyright (c) 2016-2026 Yegor Bugayenko
# SPDX-License-Identifier: MIT

SHELL := /bin/bash

.SHELLFLAGS = -e -o pipefail -c
.ONESHELL:

all:
	mvn --update-snapshots --errors --batch-mode test

clean:
	mvn clean
