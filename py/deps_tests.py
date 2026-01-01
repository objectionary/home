# SPDX-FileCopyrightText: Copyright (c) 2016-2026 Objectionary.com
# SPDX-License-Identifier: MIT

import unittest
import sys
from unittest.mock import patch  # noqa: F401
sys.path.insert(0, './py/')
from deps import dependencies

class AutoPullTest(unittest.TestCase):
    mock_file_content = """
    +rt jvm org.eolang:eo-runtime:0.29.5
    +rt jvm org.eolang:eo-files:0.4.0
    +rt jvm org.eolang:eo-hamcrest:0.4.0
    """

    @unittest.mock.patch(
        'builtins.open',
        new=unittest.mock.mock_open(read_data=mock_file_content),
        create=True
    )
    def test(self):
        self.assertEqual(
            dependencies(),
            {'eo:0.29.5', 'eo-hamcrest:0.4.0', 'eo-files:0.4.0'}
        )


if __name__ == '__main__':
    unittest.main()
