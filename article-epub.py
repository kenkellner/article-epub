#!/usr/bin/python3
import article_epub
import sys
import requests
import argparse
from bs4 import BeautifulSoup

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
        pubs = article_epub.publisher.list_publishers()
        print('Available publishers:')
        for i in pubs:
            print('• '+i.__name__)
        sys.exit()

    if args.d == None and args.u == None and args.t == None:
        sys.exit('Must provide URL, DOI or title')

    if args.d != None:
        print("Getting URL from DOI........",end='',flush=True)
        url = requests.get('https://doi.org/'+args.d,
                headers={'User-Agent':'Mozilla/5.0'}).url
        doi = args.d
        print('done')
    elif args.t != None:
        url = url_from_title(args.t)
        doi = None
    else:
        url = args.u
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
    art.epubify(args.o)
    print('\nCitation: '+art.get_citation())
    print('Filename: '+art.output)

def url_from_title(title):
    print("Getting URL from title......")
    try:
        url_stem = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C49&q="'
        search = title.replace(' ','+').replace('\n','')
        full_url = url_stem+search+'"'
        out = requests.get(full_url,headers={'User-Agent':'Mozilla/5.0'})
        soup = BeautifulSoup(out.content,'html.parser')
        result = soup.find('div',class_='gs_scl') \
            .find('div',class_='gs_ri').find('a')
        possible_title = result.text
        possible_link = result['href']

        print('Found following article:')
        print(possible_title)
        choice = input("Is this correct (y/n)? ")
        if choice == 'y':
            return(possible_link)
        else:
            sys.exit('Getting URL from title failed')
    except:
        sys.exit('Getting URL from title failed')


main()

