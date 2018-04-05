from article_epub.publisher import Publisher, register_publisher
import requests
from bs4 import BeautifulSoup

class PLoSONE(Publisher):
    """Class for PLoS ONE articles"""

    domains = ["plos.org"]

    def get_doi(self):
        if self.doi == None:
            doi_raw = self.soup.find('li',{'id':'artDoi'}).find('a') \
                .text.split('/')
            self.doi = str(doi_raw[3]+'/'+doi_raw[4])

    def get_abstract(self):
        """Get article abstract"""
        self.abstract = self.soup.find('div',class_='abstract')

    def get_keywords(self):
        """Get article keywords"""
        keywords_raw = self.soup.find('ul',{'id':'subjectList'}).find_all('li')
        self.keywords = []
        for i in keywords_raw:
            self.keywords.append(i.find('a').text)

    def get_body(self):
        """Get body of article"""
        body_raw = self.soup.find('div',class_='article-text')
        img = body_raw.find_all('div',class_='img-box')
        for i in img:
            link = i.find('a')
            new_img = 'http://journals.plos.org/plosone/'+str(link['href'])
            link.find('img')['src'] = new_img
            #link['href'] = ''

        for div in body_raw.find_all('div',class_='figure-inline-download'):
            div.decompose()

        for p in body_raw.find_all('p',class_='caption_object'):
            p.decompose()
        
        body_raw.find('div',class_='figshare_widget').decompose()

        body_parts = body_raw.find_all('div',class_='section toc-section',
            recursive=False)
        self.body = ''
        for i in body_parts:
            self.body += str(i)
    
    def get_references(self):
        """Get references list"""
        references_raw = self.soup.find('ol',class_='references')
        self.references = '<h2>References</h2>\n'+str(references_raw)

register_publisher(PLoSONE)
