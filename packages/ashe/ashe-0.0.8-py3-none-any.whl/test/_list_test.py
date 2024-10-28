import unittest

from ashe import reverse, max_count


class DictTest(unittest.TestCase):
    def setUp(self) -> None:
        self.list = ["1", "3", "1", "4"]
        self.reverse_list = ["4", "1", "3", "1"]
        self.max_count_list = "1"

    def test_reverse(self) -> None:
        self.assertEqual(reverse(self.list), self.reverse_list)

    def test_max_count(self) -> None:
        self.assertEqual(max_count(self.list), self.max_count_list)


if __name__ == "__main__":
    unittest.main()
