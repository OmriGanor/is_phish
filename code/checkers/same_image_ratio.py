import requests
from bs4 import BeautifulSoup
import os
import uuid
import cv2
from skimage.measure import compare_ssim
import time


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
    if len(url1_images) == 0:
        return 0

    for image1 in url1_images:
        if not is_valid_image(image1):
            continue
        score += max([get_image_similarity(image1, image2)
                      for image2 in url2_images if is_valid_image(image2)])
    return score / len(url1_images)


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


def same_image_ratio(url1, url2, temp_working_directory):
    # TODO: change sequence matcher to proper image comparing library
    url1_images = download_images_from_url(url1, temp_working_directory)
    url2_images = download_images_from_url(url2, temp_working_directory)
    return get_average_image_similarity(url1_images, url2_images)
