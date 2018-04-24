from article_epub.publisher import Publisher, register_publisher
import sys
import copy

class UChicago(Publisher):
    """Class for University of Chicago Press articles"""

    name = "University of Chicago Press"
    domains = ["uchicago.edu"]

    def check_fulltext(self):
        if self.soup.find('div',class_='hlFld-Fulltext') == None:
            sys.exit('Error: Can\'t access fulltext of article')
        else:
            return(True)

    def get_doi(self):
        if self.doi == None:
            self.doi = str(self.soup.find('meta',{'scheme':'doi'})['content'])

    def get_abstract(self):
        """Get article abstract"""
        abstract_raw = self.soup.find('div',class_='abstractSection')
        abstract_title = '<h2>Abstract</h2>\n'
        self.abstract = abstract_title+str(abstract_raw)

    def get_keywords(self):
        """Get article keywords"""
        self.keywords = []
        try:
            keywords_raw = self.soup \
                    .find('div',class_='hlFld-KeywordText').text
            keywords_raw = keywords_raw.strip('Keywords: ').strip('.')
            self.keywords = keywords_raw.split(',')
        except:
            pass

    def get_body(self):
        """Get body of article"""
        body_raw = copy.copy(self.soup.find('div',class_='hlFld-Fulltext'))

        for i in body_raw.find_all('div',class_='sectionHeading'):
            i.name = 'h2'

        for i in body_raw.find_all('div',class_='sectionJumpTo'):
            i.decompose()

        for i in body_raw.find_all('div',class_='head-b'):
            i.name = 'h3'

        for i in body_raw.find_all('a',class_='showFiguresEEvent'):
            try:
                i['href'] = '#'+i['data-id']
            except:
                pass

        for i in body_raw.find_all('img',{'alt':'figure'}):
            link = 'https://www.journals.uchicago.edu'+i['src']
            link = link.replace('small','medium')
            i['src'] = link

        for i in body_raw.find_all('div',class_='htmlTable'):
            i.decompose()

        for i in body_raw.find_all('span',class_='NLM_inline-graphic'):
            img = i.find('img')
            link = 'https://www.journals.uchicago.edu'+img['src']
            img['src'] = link

        self.body = str(body_raw)

    def get_references(self):
        """Get references list"""
        refs_raw = self.soup.find_all('div',class_='ref_layout')

        for i in refs_raw:
            for j in i.find_all('a'):
                j.decompose()

        refs = '<h2>Literature Cited</h2>\n'
        for i in refs_raw:
            refs += str(i)

        self.references = refs

register_publisher(UChicago)
