# SPDX-FileCopyrightText: Copyright (c) 2016-2025 Objectionary.com
# SPDX-License-Identifier: MIT

.PHONY: all clean test

all:
	make -C make
	python3 py/deps_tests.py

clean:
	make -C make clean
