# SPDX-FileCopyrightText: Copyright (c) 2016-2026 Objectionary.com
# SPDX-License-Identifier: MIT

.PHONY: all clean test

all:
	$(MAKE) -C make

clean:
	$(MAKE) -C make clean
