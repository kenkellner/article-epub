from article_epub.publisher import Publisher, register_publisher

class Springer(Publisher):
    """Class for Springer articles"""

    domains = ["springer.com"]

    def check_fulltext(self):
        if self.soup.find('div',{'id':'body'}) == None:
            print('Error: Can\'t access fulltext of article')
            sys.exit()
        else:
            return(True)
    
    def get_doi(self):
        if self.doi == None:
            doi_raw = self.soup.find('span',{"id":"doi-url"}).text.split('/')
            self.doi = str(doi_raw[-2]+'/'+doi_raw[-1])

    def get_abstract(self):
        """Get article abstract"""
        self.abstract = self.soup.find('section',class_='Abstract')

    def get_keywords(self):
        """Get article keywords"""
        keywords_raw = self.soup.find_all('span',class_='Keyword')
        self.keywords = []
        for i in keywords_raw:
            self.keywords.append(i.text.replace('\xa0',''))

    def get_body(self):
        """Get body of article"""
        self.body = self.soup.find('div',{"id":"body"})

    def get_references(self):
        """Get references list"""
        self.references = self.soup.find('section',{"id":"Bib1"})

register_publisher(Springer)
