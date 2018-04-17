from article_epub.publisher import Publisher, register_publisher
import sys

class TandF(Publisher):
    """Class for Taylor & Francis articles"""

    domains = ["tandfonline.com"]

    def get_final_url(self):
        if '/abs/' in self.url:
            self.url = self.url.replace('/abs/','/full/')
   
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
        abstract_raw.find('p',class_='summary-title').decompose()
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
        body_raw = self.soup.find_all('div',class_='NLM_sec_level_1')
        
        for i in self.soup.find_all('div',{'id':'figureViewerArticleInfo'}):
            i.decompose()

        for i in self.soup.find_all('div',{'id':'tableViewerArticleInfo'}):
            i.decompose()

        cites = self.soup.find_all('span',class_='ref-lnk')
        for i in cites:
            refid = i.find('a')['data-rid']
            i.find('a')['href'] = '#'+refid
            i.find('span',class_='ref-overlay').decompose()

        figs = self.soup.find_all('div',class_='figure')
        for i in figs:
            figid = i['id']
            i.find('div',class_='figureInfo').decompose()
            link = 'https://www.tandfonline.com'+i.find('img')['src']
            i.find('img')['src'] = link

        tabs = self.soup.find_all('div',class_='tableView')
        for i in tabs:
            try:
                i.find('h3').name = 'b'
            except:
                pass
            csv = i.find('a',{'id':'CSVdownloadButton'})
            link = 'https://www.tandfonline.com'+csv['href']
            csv['href'] = link
            i.find('a',{'id':'displaySizeTable'}).decompose()

        self.body = ''
        for i in body_raw:
            self.body += str(i)
    
    def get_references(self):
        """Get references list"""
        references_raw = self.soup.find('ul',{'id':'references-Section'})
        for i in references_raw.find_all('div',class_='xlinks-container'):
            i.decompose()
        
        references_title = '<h2>References</h2>\n'
        self.references = references_title+str(references_raw)

register_publisher(TandF)
