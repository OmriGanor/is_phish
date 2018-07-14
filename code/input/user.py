import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", help='the original website to check for phishing copies')
    parser.add_argument("-t", help='the website to check its probability to be a phishing copy of the first website')
    parser.add_argument("-l", help='log file')
    return parser.parse_args()
