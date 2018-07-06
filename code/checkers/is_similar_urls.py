"""
Author: Omri Ganor
Purpose: Checks the similarity ratio of two urls.
"""
from difflib import SequenceMatcher


def is_similar_urls(url1, url2):
    url1 = '.'.join(url1.split('.')[:-1])
    url2 = '.'.join(url2.split('.')[:-1])
    return SequenceMatcher(None, url1, url2).ratio()
