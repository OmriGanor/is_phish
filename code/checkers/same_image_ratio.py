import requests
from bs4 import BeautifulSoup
import os
import uuid
import cv2
from skimage.measure import compare_ssim
import time
from checkers.checker import Checker,CheckFailedException
import logging


class ImageSimilarityChecker(Checker):
    def __init__(self, to_check_url, original_url, temp_working_directory):
        self.logger = logging.getLogger()
        self.logger.debug("Instantiating ImageSimilarityChecker with {0} {1} {2}".format(to_check_url, original_url, temp_working_directory))
        self.temp_working_directory = temp_working_directory
        super().__init__(to_check_url, original_url)

    def run_check(self):
        try:
            self.logger.debug(
                "running ImageSimilarityChecker with {0} {1} {2}".format(self.to_check_url, self.original_url, self.temp_working_directory))
            return ImageSimilarityChecker.same_image_ratio(self.to_check_url,
                                                           self.original_url, self.temp_working_directory)
        except Exception as e:
            raise CheckFailedException("""failed to check image similarirtys between {0} and 
                                         {1} with temp working directory {2}"""
                                       .format(self.to_check_url, self.original_url, self.temp_working_directory)) from e

    @staticmethod
    def same_image_ratio(url1, url2, temp_working_directory):
        url1_images = download_images_from_url(url1, temp_working_directory)
        url2_images = download_images_from_url(url2, temp_working_directory)
        return get_average_image_similarity(url1_images, url2_images)


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
    return score


def get_average_image_similarity(url1_images, url2_images):
    score = 0
    valid_images = len(url1_images)
    if len(url1_images) == 0:
        return 0

    for image1 in url1_images:
        if not is_valid_image(image1):
            valid_images -= 1
            continue
        score += max([get_image_similarity(image1, image2)
                      for image2 in url2_images if is_valid_image(image2)])
    return score / valid_images


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



