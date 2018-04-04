from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
import os 
import sys
import pypandoc
from time import sleep
import subprocess

_publishers = list()
_publisher_domains = dict()

class Publisher(object):
    
    def __init__(self, url, doi=None, out_format='epub'):
        self.url = url
        self.doi = doi

    def soupify(self):
        """Get HTML from article's page"""
        os.environ['MOZ_HEADLESS'] = '1'
        binary = FirefoxBinary('/usr/bin/firefox')
        try:
            driver = webdriver.Firefox(firefox_binary=binary, 
                    log_path='/tmp/gecko_log')
        except:
            sys.exit('Failed to load Firefox; is it installed?')
        try:
            driver.get(self.url)
        except:
            sys.exit('Failed to load URL')
        
        if self.doi != None:
            print('Waiting for redirects..')
            sleep(5) #To allow redirects

        self.url = driver.current_url
        
        self.soup = BeautifulSoup(driver.page_source,'html.parser')
        driver.quit()

    def get_citation(self):
        
        all_authors = ''
        for i in range(0,len(self.author_surnames)):
            all_authors += self.author_surnames[i] + ', '
            all_authors += self.author_givennames[i]
            if(i != (len(self.author_surnames) - 1)):
                all_authors += '; '
        if all_authors[-1] == '.':
            cap = ' '
        else:
            cap = '. '
        
        self.citation = all_authors+cap+self.year+'. '+self.title+'. ' \
                +self.journal+' '+self.volume+': '+self.pages+'.' \
                +' doi: '+self.doi
    
    def extract_data(self):
        self.get_title()
        self.get_authors()
        self.get_abstract()
        self.get_keywords()
        self.get_metadata()
        self.get_body()
        self.get_references()
        self.get_citation()

    def epubify(self):
        """Convert data into epub format"""

        all_authors = ''
        for i in range(0,len(self.author_surnames)):
            all_authors += self.author_givennames[i] + ' '
            all_authors += self.author_surnames[i]
            if(i != (len(self.author_surnames) - 1)):
                all_authors += ', '
        
        args = []
        args.append('-M')
        args.append('title="'+self.title+'"')
        args.append('-M')
        args.append('author="'+all_authors+'"')
        args.append('--parse-raw')

        self.output = self.author_surnames[0]+'_'+self.year+'.epub'
        output_raw = '/tmp/raw.epub'

        combined = ''
        combined += str(self.citation)
        combined += str(self.abstract)
        combined += str(self.body)
        combined += str(self.references)
        
        print('Generating epub...')
        epubout = pypandoc.convert_text(combined,format='html',to='epub',
                extra_args=args,
                outputfile=output_raw)

        subprocess.check_output(['ebook-convert',output_raw,self.output])

def register_publisher(publisher):
    _publishers.append(publisher)
    for d in publisher.domains:
        _publisher_domains[d] = publisher

def get_publishers():
    return _publisher_domains

