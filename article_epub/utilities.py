import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import unquote

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
        
        if possible_title == '':
            print('No matching link available.')
            sys.exit('Getting URL from title failed')
        
        print('Provided title:')
        print(title)
        print('Found following article:')
        print(possible_title)
        choice = input("\033[0;37m"+"Is this correct (y/n)? "+"\033[00m")
        if choice == 'y':
            return(possible_link)
        else:
            sys.exit('Getting URL from title failed')
    except:
        sys.exit('Getting URL from title failed')

def url_from_doi(doi):
    print("Getting URL from DOI........",end='',flush=True)
    r = requests.get('https://doi.org/'+doi,
            headers={'User-Agent':'Mozilla/5.0'})

    #To handle Elsevier linkinghub redirects
    soup = BeautifulSoup(r.content,'html.parser')
    if soup.find('input',{'id':'redirectURL'}) is not None:
        url_raw = soup.find('input',{'id':'redirectURL'})['value']
        url = unquote(url_raw.split('_returnURL')[0])
    else:
        url = r.url

    print('done')
    return(url)
