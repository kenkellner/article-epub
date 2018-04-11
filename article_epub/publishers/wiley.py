from article_epub.publisher import Publisher, register_publisher
import sys

class Wiley(Publisher):
    """Class for Springer articles"""

    domains = ["wiley.com"]

    def get_final_url(self):
        if '/abs/' in self.url:
            self.url = self.url.replace('/abs/','/full/')
   
    def check_fulltext(self):
        test = self.soup.find_all('div',class_='article-section__content')
        if len(test) < 4:
            sys.exit('Error: Can\'t access fulltext of article')
        else:
            return(True)
    
    def get_doi(self):
        if self.doi == None:
            doi_raw = self.soup.find('a',class_='epub-doi').text.split('/')
            self.doi = str(doi_raw[3]+'/'+doi_raw[4])

    def get_abstract(self):
        """Get article abstract"""
        self.abstract = self.soup.find('section',
                class_='article-section__abstract')

    def get_keywords(self):
        """Get article keywords"""
        self.keywords = []
        try:
            keywords_raw = self.soup.find('section',class_='keywords') \
                .find_all('a',class_='badge-type')
            for i in keywords_raw:
                self.keywords.append(i.text.replace('\n','') \
                        .replace('\u200a',''))
        except:
            pass

    def get_body(self):
        """Get body of article"""
        body_raw = self.soup.find_all('div',class_='article-section__content') 
        body_raw = body_raw[1:]
        self.body = ''
        for i in body_raw:
            self.body += str(i)
    
    def get_references(self):
        """Get references list"""
        references_raw = str(self.soup.find('section',
            {'id':'references-section'}))
        references_raw = references_raw.replace('"display: none;"','')
        references_raw = references_raw.replace('Literature Cited','')
        references_raw = references_raw.replace('data-bib-id','id')
        self.references = '<h2>Literature Cited</h2>\n'+references_raw

register_publisher(Wiley)
