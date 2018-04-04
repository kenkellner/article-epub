#!/usr/bin/python3
from article_epub.publishers import ScienceDirect
import sys
import requests

def main():
    if sys.argv[1] == '-d': 
        url = requests.get('https://doi.org/'+sys.argv[2]).url
        art = ScienceDirect(url=url,doi=sys.argv[2])
    else:
        url = sys.argv[1]
        art = ScienceDirect(url=url)
    print('Downloading content...')
    art.soupify()
    art.extract_data()
    art.epubify()


main()
#test = ScienceDirect(url='https://www.sciencedirect.com/science/article/pii/S037811271630723X')

#test = ScienceDirect(url='https://www.sciencedirect.com/science/article/pii/S0946672X17308763')

#test.soupify()
#test.extract_data()
#test.epubify()

#####

#import urllib.request


#def final_url(url=None,doi=None):
#    if url !=None:
#        response = requests.get(url)
#    elif doi !=None:
#        response = request.get('https://doi.org/'+doi)
    

