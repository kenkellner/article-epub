from article_epub.sciarticle import SciArticle

class ScienceDirect(SciArticle):
    
    def get_title(self):
        self.title = self.soup.find('span',class_='title-text').text

    def get_authors(self):
        author_raw = self.soup.find('div',class_='author-group') \
            .find_all('span',class_='text surname')
        self.author_surnames = []
        for i in author_raw:
            self.author_surnames.append(i.text)

        author_raw = self.soup.find('div',class_='author-group') \
            .find_all('span',class_='text given-name')
        self.author_givennames = []
        for i in author_raw:
            self.author_givennames.append(i.text)

    def get_abstract(self):
        self.abstract = self.soup.find('div',class_='abstract author')

    def get_keywords(self):
        keys_raw = self.soup.find('div',class_='Keywords') \
            .find_all('div',class_='keyword')
        self.keywords = []
        for i in keys_raw:
            self.keywords.append(i.text)

    def get_metadata(self):
        if self.doi == None:
            doi_raw = self.soup.find('a',class_='doi').get('href').split('/')
            self.doi = doi_raw[3]+'/'+doi_raw[4]

        self.journal = self.soup.find('div',class_='publication-volume') \
            .find('span',class_='size-xl').text

        pubdate_raw = self.soup.find('div',class_='publication-volume') \
            .find('span',class_='size-m').text.split(',')

        self.year = pubdate_raw[1].split(' ')[-1]
        self.volume = pubdate_raw[0].split(' ')[1]
        self.pages = pubdate_raw[2].split(' ')[2]

    def get_body(self):
        body_raw = str(self.soup.find('div',class_='Body'))
        self.body = body_raw.replace('#b','#ref-id-b')

    def get_references(self):
        self.references = self.soup.find('section',class_='bibliography')














