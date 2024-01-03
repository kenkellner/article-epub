#!/usr/bin/env python3
import article_epub
import sys
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-u",type=str,help='URL of article',
        default=None,metavar='URL')
parser.add_argument("-d",type=str,help='DOI of article'
        ,default=None,metavar='DOI')
parser.add_argument("-t",type=str,help='Title of article',
        default=None,metavar='TITLE')
parser.add_argument("-o",type=str,help='Name of output file',
        default=None,metavar='FILE')
parser.add_argument("-p",help='List supported publishers',
        action="store_true")
args = parser.parse_args()

def main():
    if args.p:
        pubs = article_epub.list_publishers()
        print('Available publishers:')
        for i in pubs:
            print('• '+i)
        sys.exit()
    
    if args.u != None:
        url = args.u
    elif args.d != None:
        url = article_epub.url_from_doi(args.d)
    elif args.t != None:
        url = article_epub.url_from_title(args.t)
    else:
        sys.exit('Must provide URL, DOI or title')
    
    art = article_epub.match_publisher(url=url,doi=args.d)
    art.soupify()
    art.extract_data()
    art.epubify(args.o)
    print('\nCitation: '+art.get_citation())
    print('Filename: '+art.output)

if __name__ == "__main__":
    main()
