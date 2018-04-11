from article_epub.publisher import Publisher, register_publisher
import sys

class ScienceDirect(Publisher):
    """Class for Science Direct (Elsevier) articles"""

    domains = ["sciencedirect.com","elsevier.com"]

    def check_fulltext(self):
        if self.soup.find('div',class_='Body') == None:
            sys.exit('Error: Can\'t access fulltext of article')
        else:
            return(True)

    def get_doi(self):
        if self.doi == None:
            doi_raw = self.soup.find('a',class_='doi').get('href').split('/')
            self.doi = str(doi_raw[3]+'/'+doi_raw[4])

    def get_abstract(self):
        """Get article abstract"""
        self.abstract = self.soup.find('div',class_='abstract author')

    def get_keywords(self):
        """Get article keywords"""
        self.keywords = []
        try:
            keys_raw = self.soup.find('div',class_='Keywords') \
                .find_all('div',class_='keyword')
            self.keywords = []
            for i in keys_raw:
                self.keywords.append(i.text)
        except:
            pass

    def get_body(self):
        """Get body of article"""
        body_raw = str(self.soup.find('div',class_='Body'))
        self.body = body_raw.replace('#b','#ref-id-b') #Fix anchors

    def get_references(self):
        """Get references list"""
        self.references = self.soup.find('section',class_='bibliography')

register_publisher(ScienceDirect)
