#!/usr/bin/python3
import article_epub
import sys
import requests

def main():
    if sys.argv[1] == '-d': 
        url = requests.get('https://doi.org/'+sys.argv[2]).url
        doi = sys.argv[2]
    else:
        url = sys.argv[1]
        doi = None
    
    domain = url.split("//")[-1].split("/")[0].split('?')[0]

    art = article_epub.publisher.get_publishers()[domain](url=url,doi=doi)

    print('Downloading content...')
    art.soupify()
    art.extract_data()
    art.epubify()


main()

