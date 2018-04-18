from article_epub.publisher import Publisher, register_publisher
import copy
import sys

class NRC(Publisher):
    """Class for NRC Research Press articles"""

    name = "NRC Research Press"
    domains = ["nrcresearchpress.com"]
    
    def check_fulltext(self):
        if self.soup.find('div',class_='NLM_sec_level_1') == None:
            sys.exit('Error: Can\'t access fulltext of article')
        else:
            return(True)
    
    def get_doi(self):
        if self.doi == None:
            doi_raw = self.soup.find('p',class_='citationLine').find('a') \
                .text.split('/')
            self.doi = str(doi_raw[3]+'/'+doi_raw[4])

    def get_abstract(self):
        """Get article abstract"""
        abstract_raw = self.soup.find('div',class_='abstractSection')
        self.abstract = '<h2>Abstract</h2>\n'+str(abstract_raw)

    def get_keywords(self):
        """Get article keywords"""
        keywords_raw = self.soup.find('font',{'size':'-1'}).find_all('a')
        self.keywords = []
        for i in keywords_raw:
            self.keywords.append(i.text)

    def get_body(self):
        """Get body of article"""
        body_raw = copy.copy(self.soup)
        for i in body_raw.find_all('form'):
            i.decompose()
        
        figs = body_raw.find_all('a',class_='openFigLayer')
        for i in figs:
            oldlink = i.find('img')['src']
            newlink = oldlink.replace('small','medium')
            i.find('img')['src'] = 'http://nrcresearchpress.com'+newlink
            i.find('p').decompose()
        
        if len(figs) > 0:
            temp_raw = 'http://nrcresearchpress.com'+newlink
            template = temp_raw.split('f')[0:-2][0]
            for i in body_raw.find_all('div',class_='short-legend'):
                i.decompose()
            
            for i in body_raw.find_all('a',class_='openTablesLayer'):
                tabid = i['id']
                img = i.find('img')
                img['src'] = template+tabid+'.gif'
                i.find('p').decompose()
                img['width'] = ''
                img['height'] = ''
                img['align'] = ''
                img['border'] = ''
        else:
            print('Unable to get table images')
        
        for i in body_raw.find_all('alternatives'):
            link = 'http://nrcresearchpress.com'+i.find('img')['src']
            i.find('img')['src'] = link
        
        for i in body_raw.find_all('a',class_='openLayerForItem'):
            i['href'] = '#'+i['itemid']
    
        for i in body_raw.find_all('a',class_='tooltip'):
            i['href'] = '#'+i['rid']

        body_parts = body_raw.find_all('div',class_='NLM_sec_level_1')
    
        self.body = ''
        for i in body_parts:
            self.body += str(i)
    
    def get_references(self):
        """Get references list"""
        references_title = '<h2>References</h2>\n'
        references_raw = self.soup.find('ul',class_='no-bullet')
        for i in references_raw.find_all('li'):
            for j in i.find_all('a'):
                j.decompose()

        self.references = str(references_title)+str(references_raw)

register_publisher(NRC)
