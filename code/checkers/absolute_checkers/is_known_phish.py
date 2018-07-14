"""
Author: Omri Ganor
Purpose: Checks whether a url is in the known phishing DB.
"""

from checkers.checker import Checker, CheckFailedException
import logging


class KnownPhishChecker(Checker):
    def __init__(self, to_check_url, known_phish_db_path):
        self.logger = logging.getLogger()
        self.logger.debug("Instantiating KnownPhishChecker with {0} {1}".format(to_check_url, known_phish_db_path))
        self.known_phish_db_path = known_phish_db_path
        super().__init__(to_check_url, "")

    def run_check(self):
        try:
            self.logger.debug("running KnownPhishChecker with {0} {1}".format(self.to_check_url, self.known_phish_db_path))
            return KnownPhishChecker.is_known_phish(self.to_check_url, self.known_phish_db_path)
        except Exception as e:
            raise CheckFailedException("failed to check if {0} is a known phish in {1}"
                                       .format(self.to_check_url, self.known_phish_db_path)) from e

    @staticmethod
    def is_known_phish(url, path):
        with open(path, "r") as f:
            known_phish_urls = map(str.strip, f.readlines())
            return url.strip() in known_phish_urls
