"""
Author: Omri Ganor
Purpose: Checks whether two urls belong to the same domain.
"""
from urltools import compare


def is_same_domain(url1, url2):
    return compare(url1,url2)

