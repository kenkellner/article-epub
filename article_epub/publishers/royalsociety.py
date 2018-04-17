from article_epub.publisher import Publisher, register_publisher
import sys
import requests
import re
from bs4 import BeautifulSoup

class RoyalSociety(Publisher):
    """Class for Royal Society Publishing articles"""

    domains = ["royalsocietypublishing.org"]

    def check_fulltext(self):
        if self.soup.find('div',{'id':'sec-1'}) == None:
            sys.exit('Error: Can\'t access fulltext of article')
        else:
            return(True)

    def get_doi(self):
        if self.doi == None:
            self.doi = str(self.soup.find('span',
                class_='highwire-cite-metadata-doi').text.split(' ')[1])

    def get_abstract(self):
        """Get article abstract"""
        self.abstract = str(self.soup.find('div',class_='section abstract'))

    def get_keywords(self):
        """Get article keywords"""
        self.keywords = []
        try:
            keywords_raw = self.soup.find('div',
                class_='pane-node-field-highwire-article-keyword') \
                .find_all('a')
            self.keywords = []
            for i in keywords_raw:
                self.keywords.append(i.text)
        except:
            pass

    def get_body(self):
        """Get body of article"""
        body_raw = self.soup.find_all('div',{'id': re.compile('sec-.*')})

        figs = self.soup.find_all('a',class_='fragment-images')
        for j in figs:
            i = j.find('span')
            lnk = j['href']
            i.find('img')['src'] = lnk
            i.find('img')['width'] = ''
            i.find('img')['height'] = ''

        tags = self.soup.find_all('ul',class_="highwire-figure-links")
        for i in tags:
            i.find('li',class_='new-tab').decompose()
            i.find('li',class_='download-ppt').decompose()

        tables = self.soup.find_all('div',class_='table')
        for i in tables:
            try:
                src = 'http://rstb.royalsocietypublishing.org'+ \
                i.find('a')['data-table-url']
                dat = requests.get(src, headers={'User-Agent':'Mozilla/5.0'})
                tabsoup = BeautifulSoup(dat.content,'html.parser') \
                    .find('table')
                i.append(tabsoup)
                i.find('div',class_='table-callout-links').decompose()
            except:
                pass

        self.body = ''
        for i in body_raw:
            self.body += str(i)

    def get_references(self):
        """Get references list"""
        references_raw = self.soup.find('div',{'id':'ref-list-1'}).find('ol') \
            .find_all('li',recursive=False)
        ref_title = '<h2>References</h2>'

        reflist = '<ol>'
        for i in references_raw:
            try:
                tag = i.find('a')['id']
                reflist += '<li id="'+tag+'">'
                for j in i.find_all('a'):
                    j.decompose()
                reflist += i.text.replace('↵','').replace('()','')
                reflist += '</li>'
            except:
                reflist += i.text.replace('↵','')

        self.references = ref_title + reflist

register_publisher(RoyalSociety)
