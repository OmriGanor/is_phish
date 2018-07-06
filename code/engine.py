"""
Author: Omri Ganor
Purpose: Checks whether a website might be a phishing copy of another website.
"""
from checkers.static_checkers.is_known_phish import is_known_phish


def run_engine(original_url, test_url, config):
    return is_known_phish(test_url, config["checkers"]["static_checkers"]["known_phish_database_path"])

