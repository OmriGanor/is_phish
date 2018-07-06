"""
Author: Omri Ganor
Purpose: Checks whether a website might be a phishing copy of another website.
"""
from checkers.static_checkers.is_known_phish import is_known_phish
from checkers.is_same_domain import is_same_domain


def run_engine(original_url, test_url, config):
    #is_known_phish(test_url, config["checkers"]["static_checkers"]["known_phish_database_path"])
    return is_same_domain(original_url, test_url)

