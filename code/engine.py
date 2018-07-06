"""
Author: Omri Ganor
Purpose: Checks whether a website might be a phishing copy of another website.
"""
from checkers.static_checkers.is_known_phish import is_known_phish


def run_engine(original_url, test_url):
    return is_known_phish(test_url)
