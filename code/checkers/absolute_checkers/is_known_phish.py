"""
Author: Omri Ganor
Purpose: Checks whether a url is in the known phishing DB.
"""

from checkers.checker import Checker


class KnowPhishChecker(Checker):
    def __init__(self, to_check_url, known_phish_db_path):
        self.known_phish_db_path = known_phish_db_path
        super().__init__(to_check_url, "")

    def run_check(self):
        return KnowPhishChecker.is_known_phish(self.to_check_url, self.known_phish_db_path)

    @staticmethod
    def is_known_phish(url, path):
        with open(path, "r") as f:
            known_phish_urls = map(str.strip, f.readlines())
            return url.strip() in known_phish_urls


