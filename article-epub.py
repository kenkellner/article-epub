#!/usr/bin/python3
import article_epub
import sys
import requests

def main():
    if sys.argv[1] == '-d':
        print("Getting URL from DOI........",end='',flush=True)
        url = requests.get('https://doi.org/'+sys.argv[2]).url
        doi = sys.argv[2]
        print('done')
    else:
        url = sys.argv[1]
        doi = None
    
    domain = ".".join(url.split("//")[-1].split("/")[0] \
            .split('?')[0].split('.')[-2:])

    try:
        art = article_epub.publisher.get_publishers()[domain](url=url,doi=doi)
    except:
        sys.exit('Publisher not supported.')

    art.soupify()
    art.extract_data()
    art.epubify()
    print('\nCitation: '+art.citation)
    print('Filename: '+art.output)


main()

