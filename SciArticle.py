#!/usr/bin/python3
#https://github.com/mozilla/geckodriver/releases
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
import re
import os 
import sys
import pypandoc
from time import sleep

class SciArticle(object):
    
    def __init__(self, url, doi=None, out_format='kepub'):
        self.url = url
        self.output_format = out_format
        if out_format not in ['epub','kepub']:
            sys.exit('Supported formats are epub and kepub')
        if doi != None:
            self.doi = doi

    def soupify(self):
        """Get HTML from article's page"""
        os.environ['MOZ_HEADLESS'] = '1'
        binary = FirefoxBinary('/usr/bin/firefox')
        try:
            driver = webdriver.Firefox(firefox_binary=binary, log_file='/tmp/gecko_log')
        except:
            sys.exit('Failed to load Firefox; is it installed?')
        try:
            driver.get(self.init_url)
        except:
            sys.exit('Failed to load URL')
        
        sleep(2) #To allow redirects
        self.url = driver.current_url
        
        self.soup = BeautifulSoup(driver.page_source,'html.parser')
        driver.quit()
        #return(self.soup)

    #def out_filename(self):
    #    first5 = self.title.split()[:5]


    def epubify(self):
        """Convert data into epub format"""
        args = []
        args.append('-M')
        args.append('title="'+self.title+'"')
        args.append('author="'+author+'"')
        args.append('--parse-raw')

        epubout = pypandoc.convert_text(self.body,format='html',to='epub',
                extra_args=args,
                outputfile=self.output)






