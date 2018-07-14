"""
Author: Omri Ganor
Purpose: Checks whether a website might be a phishing copy of another website.
"""
from checkers.absolute_checkers.is_same_domain import SameDomainsChecker
from checkers.absolute_checkers.is_known_phish import KnownPhishChecker
from checkers.is_long_url import LongUrlChecker
from checkers.is_similar_urls import SimilarUrlsChecker
from checkers.same_image_ratio import ImageSimilarityChecker
from checkers.phishy_words_ratio import PhishyWordsChecker
import os


def run_engine(original_url, test_url, config):
    known_phish_checker = KnownPhishChecker(test_url, os.path.join(os.path.dirname(os.path.abspath(__file__)), config["checkers"]["absolute_checkers"]["known_phish_database_path"]))
    same_domain_checker = SameDomainsChecker(original_url, test_url)
    long_url_checker = LongUrlChecker(test_url, config["checkers"]["long_url_length"])
    similar_urls_checker = SimilarUrlsChecker(original_url, test_url)
    image_similarity_checker = ImageSimilarityChecker(original_url, test_url, r"C:\temp")
    phishy_words_checker = PhishyWordsChecker(test_url, os.path.join(os.path.dirname(os.path.abspath(__file__)), config["checkers"]["phishy_words_database_path"]))
    return None
