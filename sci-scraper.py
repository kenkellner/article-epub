#!/usr/bin/python3

from article_epub.publishers import ScienceDirect


test = ScienceDirect(url='https://www.sciencedirect.com/science/article/pii/S037811271630723X')

test = ScienceDirect(url='https://www.sciencedirect.com/science/article/pii/S0946672X17308763')

test.soupify()
test.extract_data()
test.epubify()

#####

import urllib.request


def final_url(url=None,doi=None):
    if url !=None:
        response = requests.get(url)

