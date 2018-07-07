import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher


def get_images_from_site(site):
    images = []
    response = requests.get(site)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    urls = [img['src'] for img in img_tags]

    for url in urls:
        if 'http' not in url:
            # sometimes an image source can be relative
            # if it is provide the base url which also happens
            # to be the site variable atm.
            url = '{}{}'.format(site, url)
        response = requests.get(url)
        images.append(response.content)


def same_image_ratio(url1, url2):
    # TODO: change sequence matcher to proper image comparing library
    return SequenceMatcher(None, get_images_from_site(url1), get_images_from_site(url2)).ratio()
