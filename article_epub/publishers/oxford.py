from article_epub.publisher import Publisher, register_publisher
import copy
import sys

class Oxford(Publisher):
    """Class for Oxford articles"""

    domains = ["oup.com"]

    def check_fulltext(self):
        if self.soup.find('div',{'data-widgetname':'ArticleFulltext'}) == None:
            sys.exit('Error: Can\'t access fulltext of article')
        else:
            return(True)
    
    def get_doi(self):
        if self.doi == None:
            doi_raw = self.soup.find('div',class_='ww-citation-primary') \
                .find('a')['href'].split('/')
            self.doi = str(doi_raw[3]+'/'+doi_raw[4])

    def get_abstract(self):
        """Get article abstract"""
        abstract_raw = self.soup.find('section',class_='abstract')
        self.abstract = '<h2>Abstract</h2>\n'+str(abstract_raw)

    def get_keywords(self):
        """Get article keywords"""
        self.keywords = []
        try:
            keywords_raw = self.soup.find('div',class_='kwd-group') \
                .find_all('a')
            for i in keywords_raw:
                self.keywords.append(i.text)
        except:
            pass

    def get_body(self):
        """Get body of article"""
        body_raw = copy.copy(self.soup.find(
            'div',{'data-widgetname':'ArticleFulltext'}))
        body_raw.find('h2',class_='abstract-title').decompose()
        body_raw.find('section',class_='abstract').decompose()
        body_raw.find('div',class_='article-metadata-panel').decompose()
        body_raw.find('div',class_='ref-list').decompose()
        body_raw.find('span',{'id':'UserHasAccess'}).decompose()
        body_raw.find('div',class_='copyright').decompose()
        body_raw.find('h2',class_='backreferences-title').decompose()

        for i in body_raw.find_all('div',class_='fig-modal'):
            i.decompose()

        for i in body_raw.find_all('div',class_='table-modal'):
            i.decompose()
        
        for i in body_raw.find_all('div',class_='fig-orig'):
            i.decompose()

        for i in body_raw.find_all('a',class_='fig-view-orig'):
            i.decompose()

        for i in body_raw.find_all('a',class_='xref-bibr'):
            new = '#'+i['reveal-id']
            i['href'] = new
        
        for i in body_raw.find_all('a',class_='xref-fig'):
            new = '#'+i['reveal-id']
            i['href'] = new
        
        self.body = body_raw
    
    def get_references(self):
        """Get references list"""
        references_title = self.soup.find('h2',class_='backreferences-title')
        references_raw = self.soup.find('div',class_='ref-list')
        refs_format = ''
        for i in references_raw.find_all('div',recursive=False):
            for j in i.find_all('a'):
                j.decompose()
            refs_format += '<div id="'+i['content-id']+'">'
            refs_format += i.text+'\n</div>'

        self.references = str(references_title)+str(refs_format)
        self.references = self.references.replace('doi:','')

register_publisher(Oxford)
