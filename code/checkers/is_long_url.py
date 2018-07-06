"""
Author: Omri Ganor
Purpose: Checks whether a url is long. Phishing urls are often very long.
"""


def is_long_url(url, length):
    return len(url) > length
