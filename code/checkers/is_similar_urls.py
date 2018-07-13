"""
Author: Omri Ganor
Purpose: Checks the similarity ratio of two urls.
"""
from difflib import SequenceMatcher
from checkers.checker import Checker


class SimilarUrlsChecker(Checker):
    def __init__(self, to_check_url, original_url):
        super().__init__(to_check_url, original_url)

    def run_check(self):
        return SimilarUrlsChecker.is_similar_urls(self.to_check_url, self.original_url)

    @staticmethod
    def is_similar_urls(url1, url2):
        url1 = '.'.join(url1.split('.')[:-1])
        url2 = '.'.join(url2.split('.')[:-1])
        return SequenceMatcher(None, url1, url2).ratio()


