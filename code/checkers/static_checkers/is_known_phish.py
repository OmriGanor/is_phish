"""
Author: Omri Ganor
Purpose: Checks whether a url is in the known phishing DB.
"""


def is_known_phish(url, path):
    with open(path, "r") as f:
        known_phish_urls = map(str.strip, f.readlines())
        return url.strip() in known_phish_urls
