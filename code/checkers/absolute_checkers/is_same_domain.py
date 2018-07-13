"""
Author: Omri Ganor
Purpose: Checks whether two urls belong to the same domain.
"""
from urltools import compare
from checkers.checker import Checker


class SameDomainsChecker(Checker):
    def __init__(self, to_check_url, original_url):
        super().__init__(to_check_url, original_url)

    def run_check(self):
        return SameDomainsChecker.is_same_domain(self.to_check_url, self.original_url)

    @staticmethod
    def is_same_domain(url1, url2):
        return compare(url1, url2)




