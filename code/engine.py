"""
Author: Omri Ganor
Purpose: Checks whether a website might be a phishing copy of another website.
"""
from checkers.absolute_checkers.is_same_domain import is_same_domain
from checkers.absolute_checkers.is_known_phish import is_known_phish
from checkers.is_long_url import is_long_url


def run_engine(original_url, test_url, config):
    is_known_phish(test_url, config["checkers"]["static_checkers"]["known_phish_database_path"])
    is_same_domain(original_url, test_url)
    return is_long_url(test_url, config["checkers"]["long_url_length"])


