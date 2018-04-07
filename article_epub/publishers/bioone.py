from article_epub.publisher import Publisher, register_publisher
import requests
from bs4 import BeautifulSoup

class BioOne(Publisher):
    """Class for BioOne articles"""

    domains = ["bioone.org"]
    
    def check_fulltext(self):
        if self.soup.find('div',class_='hlFld-Fulltext') == None:
            print('Error: Can\'t access fulltext of article')
            sys.exit()
        else:
            return(True)

    def get_final_url(self):
        if '/abs/' in self.url:
            self.url = self.url.replace('/doi/abs/','/doi/')

    def get_doi(self):
        if self.doi == None:
            doi_raw = self.soup.find('p',class_='articleRef') \
                .find('a').text.split('/')
            self.doi = str(doi_raw[3]+'/'+doi_raw[4])

    def get_abstract(self):
        """Get article abstract"""
        abstract_raw = str(self.soup.find('div',class_='abstractSection'))
        self.abstract = abstract_raw.replace('<h3','<h2') \
                .replace('</h3>','</h2>').replace('Abstract. ','ABSTRACT')

    def get_keywords(self):
        """Get article keywords"""
        pass

    def get_body(self):
        """Get body of article"""
        body_full = self.soup.find('div',class_='hlFld-Fulltext')
        links_old = body_full.find_all('a',class_='ref')
        for i in links_old:
            try:
                tag = '#'+i['onclick'].split("'")[1]
                i['href'] = str(tag)
                i['onclick'] = ''
            except:
                pass
        
        print('Downloading higher-quality images...')
        imgs_old = body_full.find_all('div',class_='articleImage')
        for i in imgs_old:
            try:
                link = i.find('a',class_='popupLink') 
                imgpage = BeautifulSoup(requests.get('https://bioone.org' \
                   +str(link['href'])).content,'html.parser')
                imglink = 'http://bioone.org'+str(imgpage.find('img')['src'])
                link.find('img')['src'] = imglink
                link['href'] = ''
            except:
                pass

        body_raw = body_full.find_all('div',class_='NLM_sec_level_1')
        self.body = ''
        for i in body_raw:
            self.body += str(i)

        self.body = self.body.replace('<h6>','<h2>').replace('</h6>','</h2>')
        self.body = self.body.replace('enlarge figure','')
    
    def get_references(self):
        """Get references list"""
        references_raw = str(self.soup.find('div',class_='articleReferences'))
        self.references = references_raw.replace('<h3>','<h2>') \
                .replace('</h3>','</h2>')

register_publisher(BioOne)
