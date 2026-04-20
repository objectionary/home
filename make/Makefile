# SPDX-FileCopyrightText: Copyright (c) 2016-2026 Yegor Bugayenko
# SPDX-License-Identifier: MIT

SHELL := /bin/bash

.SHELLFLAGS = -e -o pipefail -c
.ONESHELL:

DIRS := $(wildcard */.)

all:
	for d in $(DIRS); do
		cd $${d} && make && cd ..
	done

clean:
	git clean -fdX
	for d in $(DIRS); do
		cd $${d} && make clean && cd ..
	done
