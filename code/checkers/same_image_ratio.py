"""
Author: Omri Ganor
Purpose: Checks the image similarity ratio between to websites.
"""
import requests
from bs4 import BeautifulSoup
import os
import uuid
import cv2
from skimage.measure import compare_ssim
import time
from checkers.checker import Checker, CheckFailedException
import logging


class ImageSimilarityChecker(Checker):
    def __init__(self, to_check_url, original_url, temp_working_directory, weight):
        self.logger = logging.getLogger()
        self.logger.debug("Instantiating ImageSimilarityChecker with {0} {1} {2}".format(to_check_url, original_url, temp_working_directory))
        self.temp_working_directory = temp_working_directory
        super().__init__(to_check_url, original_url, weight)

    def run_check(self):
        try:
            self.logger.debug(
                "running ImageSimilarityChecker with {0} {1} {2}".format(self.to_check_url, self.original_url, self.temp_working_directory))
            return ImageSimilarityChecker.same_image_ratio(self.to_check_url,
                                                           self.original_url, self.temp_working_directory)
        except CheckFailedException:
            self.logger.error(
                "failed to check image similarirtys between {0} and {1} with temp working directory {2}"
                    .format(self.to_check_url, self.original_url, self.temp_working_directory)
            )
            raise

    @staticmethod
    def same_image_ratio(to_check_url, original_url, temp_working_directory):
        to_check_url = download_images_from_url(to_check_url, temp_working_directory)
        original_url = download_images_from_url(original_url, temp_working_directory)
        return ImageSimilarityChecker.get_average_image_similarity(to_check_url, original_url)

    @staticmethod
    def get_average_image_similarity(to_check_url_images, original_url_images):
        score = 0
        valid_images = len(to_check_url_images)
        if len(original_url_images) == 0 and len(to_check_url_images) == 0:
            return 1
        elif len(original_url_images) == 0 and not len(to_check_url_images) == 0 or \
                len(original_url_images) != 0 and len(to_check_url_images) == 0:
            return 0

        for image1 in to_check_url_images:
            if not is_valid_image(image1):
                valid_images -= 1
                continue
            image_similarities = [get_image_similarity(image1, image2) for image2 in original_url_images if
                                  is_valid_image(image2)]
            score += max(image_similarities)

        if len(valid_images) == 0:
            raise CheckFailedException("No valid images to compare")
        return score / valid_images


def is_valid_image(path):
    return path is not None and cv2.imread(path) is not None


def get_image_similarity(path1, path2):
    # load the two input images
    image1 = cv2.imread(path1)
    image2 = cv2.imread(path2)

    if image1.shape != image2.shape:
        width = int(image1.shape[1])
        height = int(image1.shape[0])
        dim = (width, height)
        image2 = cv2.resize(image2, dim, interpolation=cv2.INTER_AREA)

    # convert the images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two images.
    # returns a score between -1 to 1 with 1 being a perfect match.
    score = compare_ssim(gray1, gray2)
    return (score + 1) / 2.0  # normalize score to be between 0 and 1


def download_file(url, download_directory):
    local_filename = str(uuid.uuid4())
    r = requests.get(url, stream=True)
    file_path = os.path.join(download_directory, local_filename)
    with open(file_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return file_path


def download_images_from_url(url, temp_directory):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    images_directory = os.path.join(temp_directory, str(uuid.uuid4()))
    os.makedirs(images_directory)
    images = []
    for link in soup.findAll('img'):
        image_links = link.get('src')
        if not image_links.startswith('http'):
            image_links = url + '/' + image_links
        images.append(download_file(image_links, images_directory))
        time.sleep(3)
    return images



