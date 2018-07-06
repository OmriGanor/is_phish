import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", help='the original website to check for phishing copies')
    parser.add_argument("-t", help='the website to check its probability to be a phising copy of the first website')
    return parser.parse_args()
