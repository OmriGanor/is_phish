"""
Author: Omri Ganor
Purpose: Checks whether a url is long. Phishing urls are often very long.
"""
from checkers.checker import Checker,CheckFailedException


class LongUrlChecker(Checker):
    def __init__(self, to_check_url, long_url_length):
        self.long_url_length = long_url_length
        super().__init__(to_check_url, "")

    def run_check(self):
        try:
            return LongUrlChecker.is_long_url(self.to_check_url, self.long_url_length)
        except Exception as e:
            raise CheckFailedException("failed to check if {0} is longer than {1}"
                                       .format(self.to_check_url, self.long_url_length)) from e

    @staticmethod
    def is_long_url(url, length):
        return len(url) > length
