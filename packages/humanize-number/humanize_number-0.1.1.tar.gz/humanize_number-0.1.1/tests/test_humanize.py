import unittest
from humanize_number import humanize_number

class TestHumanizeNumber(unittest.TestCase):
    def test_humanize_number(self):
        self.assertEqual(humanize_number(1000), '1K')
        self.assertEqual(humanize_number(1000000), '1M')
        self.assertEqual(humanize_number(1000000000), '1B')
        self.assertEqual(humanize_number(1000000000000), '1T')

if __name__ == '__main__':
    unittest.main()