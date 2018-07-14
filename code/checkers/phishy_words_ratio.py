"""
Author: Omri Ganor
Purpose: Checks the amount of occurrences of phishy words in the website we are testing.
"""
from checkers.checker import Checker
import requests


class PhishyWordsChecker(Checker):
    def __init__(self, to_check_url, phishy_words_path):
        self.phishy_words_path = phishy_words_path
        super().__init__(to_check_url, "")

    def run_check(self):
        return PhishyWordsChecker.phishy_words_ratio(self.to_check_url, self.phishy_words_path)

    @staticmethod
    def phishy_words_ratio(url1, phishy_words_path):
        with open(phishy_words_path, "r") as f:
            phishy_words = list(map(str.strip, f.readlines()))
            return PhishyWordsChecker.has_words(url1, phishy_words)

    @staticmethod
    def has_words(url, words):
        result = 0
        text = requests.get(url, allow_redirects=False).text.lower()
        for the_word in words:
            if the_word in text:
                result += 1
        return result / len(words)







