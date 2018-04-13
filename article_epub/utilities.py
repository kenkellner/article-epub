import requests
from bs4 import BeautifulSoup
import sys

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
        print('Provided title:')
        print(title)
        print('Found following article:')
        print(possible_title)
        choice = input("Is this correct (y/n)? ")
        if choice == 'y':
            return(possible_link)
        else:
            sys.exit('Getting URL from title failed')
    except:
        sys.exit('Getting URL from title failed')

