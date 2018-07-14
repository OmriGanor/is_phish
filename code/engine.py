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
from checkers.checker import CheckFailedException
import logging
import os


def create_checkers(original_url, test_url, config):
    checkers = []
    checkers.append(
        LongUrlChecker(test_url, config["checkers"]["long_url_length"],
                       config["checkers"]["weights"]["LongUrlChecker"]))
    checkers.append(
        SimilarUrlsChecker(original_url, test_url, config["checkers"]["weights"]["SimilarUrlsChecker"]))
    checkers.append(
        ImageSimilarityChecker(original_url, test_url, config["checkers"]["temp_working_directory"],
                               config["checkers"]["weights"]["ImageSimilarityChecker"]))
    checkers.append(
        PhishyWordsChecker(test_url,
                           os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        config["checkers"]["phishy_words_database_path"]),
                           config["checkers"]["weights"]["PhishyWordsChecker"]))
    return checkers


def run_engine(original_url, test_url, config):
    result = 0
    result_accuracy = 0
    logger = logging.getLogger()
    known_phish_checker = KnownPhishChecker(test_url,
                                            os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                         config["checkers"]["absolute_checkers"]["known_phish_database_path"]))
    same_domain_checker = SameDomainsChecker(original_url, test_url)

    try:
        is_known_phish = known_phish_checker.run_check()
    except CheckFailedException as e:
        logger.error("failed checking if {0} is known phish".format(known_phish_checker.to_check_url), str(e))
    if is_known_phish:
        return 1, 1

    """
    try:
        is_same_domain = same_domain_checker.run_check()
    except CheckFailedException as e:
        logger.error("failed checking if {0} and {1} are same domain"
                     .format(same_domain_checker.to_check_url, same_domain_checker.original_url), str(e))
    if is_same_domain:
        return 0, 1
    """

    checkers = create_checkers(original_url, test_url, config)
    for checker in checkers:
        try:
            check_result = checker.run_check()
            logger.debug("Checker returned result {0} with weight {1}".format(check_result, checker.weight))
        except CheckFailedException as e:
            logger.error(e)
            continue
        else:
            result += check_result * checker.weight
            result_accuracy += checker.weight

    return result/result_accuracy, result_accuracy
