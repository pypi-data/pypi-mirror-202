import unittest
from ez_bar import ProgressBar
from ez_bar.bar_styles import BarColors, BarStyles


class ProgressBarTestCase(unittest.TestCase):
    def setUp(self):
        self.range = range(5000)
        self.test_list = ["a", "b", "c", "d", "e", "f"]
        self.test_dict = {
            "1": {
                "a": "b"
            },
            "2": {
                "c": "d"
            },
            "3": {
                "e": "f"
            }
        }
        self.progress_bar = ProgressBar(show_fractions=True, color=BarColors.GREEN, style=BarStyles.DEFAULT)

    def test_progress_bar_for_range(self):
        for i in self.range:
            self.progress_bar(index=i, iterable=self.range, current=i)

    def test_progress_bar_for_list(self):
        for i, v in enumerate(self.test_list):
            self.progress_bar(index=i, iterable=self.test_list, current=v)

    def test_progress_bar_for_dict(self):
        for i, (k, v) in enumerate(self.test_dict.items()):
            self.progress_bar(index=i, iterable=self.test_dict, current=v)


if __name__ == '__main__':
    unittest.main()
