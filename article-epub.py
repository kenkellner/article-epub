#!/usr/bin/python3
import article_epub
import sys
import requests
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-u","--url",type=str,help='URL of article',default=None)
parser.add_argument("-d","--doi",type=str,help='DOI of article',default=None)
parser.add_argument("-o","--out",type=str,help='Name of output file',
        default=None,metavar='FILE')
parser.add_argument("-p","--publishers",help='List supported publishers',
        action="store_true")
args = parser.parse_args()

def main():

    if args.publishers:
        pubs = article_epub.publisher.list_publishers()
        print('Available publishers:')
        for i in pubs:
            print('• '+i.__name__)
        sys.exit()

    if args.doi == None and args.url == None:
        sys.exit('Must provide either URL or DOI')

    if args.doi != None:
        print("Getting URL from DOI........",end='',flush=True)
        url = requests.get('https://doi.org/'+args.doi).url
        doi = args.doi
        print('done')
    else:
        url = args.url
        doi = None
    
    domain = ".".join(url.split("//")[-1].split("/")[0] \
            .split('?')[0].split('.')[-2:])

    try:
        art = article_epub.publisher.get_publishers()[domain](url=url,doi=doi)
        print('Matched URL to publisher: '+art.__class__.__name__)
    except:
        sys.exit('Publisher not supported.')

    art.soupify()
    art.extract_data()
    art.epubify(args.out)
    print('\nCitation: '+art.citation)
    print('Filename: '+art.output)


main()

