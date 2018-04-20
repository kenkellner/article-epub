from article_epub.publisher import Publisher, register_publisher
import sys
import copy

class Nature(Publisher):
    """Class for Nature Publishing articles"""

    name = "Nature Publishing"
    domains = ["nature.com"]

    def check_fulltext(self):
        test = self.soup.find('a',{'data-track-action':'subscribe'})
        if test != None:
            sys.exit('Error: Can\'t access fulltext of article')
        else:
            return(True)

    def get_doi(self):
        if self.doi == None:
            self.doi = str(self.soup.find('meta',{'name':'DOI'})['content'])

    def get_abstract(self):
        """Get article abstract"""
        abstract_raw = self.soup.find('div',{'id':'abstract-section'})
        try:
            abstract_raw.find('span').decompose()
        except:
            pass

        self.abstract = str(abstract_raw)

    def get_keywords(self):
        """Get article keywords"""
        self.keywords = []
        try:
            keywords_raw = self.soup.find_all('a',class_='subject-tag-link')
            for i in keywords_raw:
                self.keywords.append(i.text)
        except:
            pass

    def get_body(self):
        """Get body of article"""
        body_raw = copy.copy(self.soup.find('div',class_='article-body'))

        try:
            body_raw.find('section',{'aria-labelledby':'abstract'}).decompose()
        except:
            pass

        try:
            body_raw.find('section',{'aria-labelledby':'references'}).decompose()
        except:
            pass

        try:
            body_raw.find('section', \
                    {'aria-labelledby':'author-information'}).decompose()
            body_raw.find('section',{'aria-labelledby':'rightslink'}) \
                    .decompose()
            body_raw.find('section',{'aria-labelledby':'article-comments'}) \
                    .decompose()
        except:
            pass

        for i in body_raw.find_all('span',class_='js-section-title-label'):
            i.decompose()

        for i in body_raw.find_all('a',{'data-track-action':'view table'}):
            link = 'https://www.nature.com'+i['href']
            i['href'] = link

        for i in body_raw.find_all('a',{'data-track-action':'reference anchor'}):
            part = i['href'].split('#')[1]
            i['href'] = '#'+part

        for i in body_raw.find_all('a',{'data-track-action':'view figure'}):
            link = 'https://www.nature.com'+i['href']
            i['href'] = link

        self.body = str(body_raw)

    def get_references(self):
        """Get references list"""
        ref_all = self.soup.find('div',{'id':'references-section'})
        ref_all.find('span',class_='js-section-title-label').decompose()
        refs = ref_all.find('ol').find_all('li',recursive=False)
        for i in refs:
            try:
                i.find('span').decompose()
                i.find('ul',class_='js-ref-links').decompose()
            except:
                pass

        self.references = str(ref_all)

register_publisher(Nature)
