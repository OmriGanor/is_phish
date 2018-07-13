"""
Author: Omri Ganor
Purpose: Checks whether a url is long. Phishing urls are often very long.
"""
from checkers.checker import Checker


class LongUrlChecker(Checker):
    def __init__(self, to_check_url, long_url_length):
        self.long_url_length = long_url_length
        super().__init__(to_check_url, "")

    def run_check(self):
        return LongUrlChecker.is_long_url(self.to_check_url, self.long_url_length)

    @staticmethod
    def is_long_url(url, length):
        return len(url) > length
