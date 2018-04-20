from article_epub.publisher import Publisher, register_publisher
import sys
import copy
import requests

class AnnualReviews(Publisher):
    """Class for Annual Reviews articles"""

    name = "Annual Reviews"
    domains = ["annualreviews.org"]

    def get_final_url(self):
        pass
   
    def check_fulltext(self):
        test = self.soup.find_all('div',class_='hlFld-Fulltext')
        if len(test) < 1:
            sys.exit('Error: Can\'t access fulltext of article')
        else:
            return(True)
    
    def get_doi(self):
        if self.doi == None:
            self.doi = str(self.soup.find('meta',{'scheme':'doi'})['content'])
            
    def get_abstract(self):
        """Get article abstract"""
        abstract_raw = self.soup.find('div',class_='hlFld-Abstract')
        try:
            abstract_raw.find('iframe').decompose()
        except:
            pass
        try:
            abstract_raw.find('span',class_='title').decompose()
        except:
            pass
        
        self.abstract = str(abstract_raw)

    def get_keywords(self):
        """Get article keywords"""
        self.keywords = []
        try:
            keywords_raw = self.soup.find('div',class_='hlFld-KeywordText') \
                .find_all('a')
            for i in keywords_raw:
                self.keywords.append(i.text)
        except:
            pass

    def get_body(self):
        """Get body of article"""
        body_raw = copy.copy(self.soup.find('div',class_='hlFld-Fulltext'))

        try:
            body_raw.find('div',class_='lit-cited').decompose()
            body_raw.find('div',{'id':'citations'}).decompose()
        except:
            pass

        for i in body_raw.find_all('a',class_='scrollRef'):
            i['href'] = '#'+i['refid']+'ref'

        for i in body_raw.find_all('a',class_='scrollFig'):
            try:
                i['href'] = '#'+i['data-figindex']
            except:
                pass

        for i in body_raw.find_all('figure'):
            oldlink = 'https://www.annualreviews.org'+ \
                    i.find('a').find('img')['src']
            newlink = oldlink.replace('small','medium')
            response = requests.head(newlink).headers['content-type']
            if 'image' in response:
                i.find('a').find('img')['src'] = newlink
            else:
                newlinkjpeg = newlink.replace('.gif','.jpeg')
                i.find('a').find('img')['src'] = newlinkjpeg
        
        for i in body_raw.find_all('span',class_='NLM_inline-graphic'):
            link = 'https://www.annualreviews.org'+\
                    i.find('img')['src']
            i.find('img')['src'] = link

        for i in body_raw.find_all('div',class_='equation'):
            link = 'https://www.annualreviews.org'+i.find('img')['src']
            i.find('img')['src'] = link

        self.body = str(body_raw)
    
    def get_references(self):
        """Get references list"""
        references = self.soup.find('div',class_='lit-cited')

        for i in references.find_all('ul',class_='off-links'):
            i.decompose()
        for i in references.find_all('div',class_='article-locations'):
            i.decompose()
        for i in references.find_all('a',class_='ar-modal-link citation'):
            i.decompose()
        for i in references.find_all('div',class_='citation-content'):
            i.decompose()

        self.references = str(references)

register_publisher(AnnualReviews)
