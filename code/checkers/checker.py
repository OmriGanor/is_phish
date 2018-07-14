"""
Author: Omri Ganor
Purpose: serves as an abstract checker that all checkers need to implement.
"""


class CheckFailedException(Exception):
    pass


class Checker(object):
    def __init__(self, to_check_url, original_url):
        self.to_check_url = to_check_url
        self.original_url = original_url

    def run_check(self):
        raise NotImplementedError("""This method needs to be implemented by each checker. 
                                    Should return a result between 0 - no similarity to 1 - identical.""")
