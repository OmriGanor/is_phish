"""
Author: Omri Ganor
Purpose: Checks the similarity ratio of two urls.
"""
from difflib import SequenceMatcher
from checkers.checker import Checker,CheckFailedException
import logging


class SimilarUrlsChecker(Checker):
    def __init__(self, to_check_url, original_url):
        self.logger = logging.getLogger()
        self.logger.debug("Instantiating SimilarUrlsChecker with {0} {1}".format(to_check_url, original_url))
        super().__init__(to_check_url, original_url)

    def run_check(self):
        try:
            self.logger.debug(
                "running SimilarUrlsChecker with {0} {1}".format(self.to_check_url, self.original_url))
            return SimilarUrlsChecker.is_similar_urls(self.to_check_url, self.original_url)
        except Exception as e:
            raise CheckFailedException("failed to check if {0} is similar to {1}"
                                       .format(self.to_check_url, self.original_url)) from e

    @staticmethod
    def is_similar_urls(url1, url2):
        url1 = '.'.join(url1.split('.')[:-1])
        url2 = '.'.join(url2.split('.')[:-1])
        return SequenceMatcher(None, url1, url2).ratio()


