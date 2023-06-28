import unittest
from unittest.mock import patch
import sys
sys.path.insert(0, './py/')
from deps import dependencies

class AutoPullTest(unittest.TestCase):
    mock_file_content = """
    +rt jvm org.eolang:eo-runtime:0.29.5
    """

    @unittest.mock.patch(
        'builtins.open',
        new=unittest.mock.mock_open(read_data=mock_file_content),
        create=True
    )
    def test(self):
        self.assertEqual(
            dependencies(),
            {'eo:0.29.5'}
        )
        print(dependencies())


if __name__ == '__main__':
    unittest.main()
