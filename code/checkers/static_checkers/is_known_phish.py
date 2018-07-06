"""
Author: Omri Ganor
Purpose: Checks whether a url is in the known phishing DB.
"""


def is_known_phish(url, path):
    with open(path, "rb") as f:
        known_phish_urls = f.readlines()
        return url in known_phish_urls
