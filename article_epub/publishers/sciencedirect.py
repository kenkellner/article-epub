from article_epub.publisher import Publisher, register_publisher

class ScienceDirect(Publisher):
    """Class for Science Direct (Elsevier) articles"""

    domains = ["sciencedirect.com","www.sciencedirect.com",
            "linkinghub.elsevier.com"]
    
    def get_title(self):
        """Get article title"""
        self.title = self.soup.find('span',class_='title-text').text

    def get_authors(self):
        """Get author given and surnammes"""
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
        """Get article abstract"""
        self.abstract = self.soup.find('div',class_='abstract author')

    def get_keywords(self):
        """Get article keywords"""
        keys_raw = self.soup.find('div',class_='Keywords') \
            .find_all('div',class_='keyword')
        self.keywords = []
        for i in keys_raw:
            self.keywords.append(i.text)

    def get_metadata(self):
        """Get assortment of other metadata"""
        if self.doi == None:
            doi_raw = self.soup.find('a',class_='doi').get('href').split('/')
            self.doi = doi_raw[3]+'/'+doi_raw[4]

        self.journal = self.soup.find('div',class_='publication-volume') \
            .find('span',class_='size-xl').text

        pubdate_raw = self.soup.find('div',class_='publication-volume') \
            .find('span',class_='size-m').text.split(',')

        self.year = pubdate_raw[-2].split(' ')[-1]
        self.volume = pubdate_raw[0].split(' ')[1]
        self.pages = pubdate_raw[-1].split(' ')[2]

    def get_body(self):
        """Get body of article"""
        body_raw = str(self.soup.find('div',class_='Body'))
        self.body = body_raw.replace('#b','#ref-id-b') #Fix anchors

    def get_references(self):
        """Get references list"""
        self.references = self.soup.find('section',class_='bibliography')

register_publisher(ScienceDirect)
