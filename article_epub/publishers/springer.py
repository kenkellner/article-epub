from article_epub.publisher import Publisher, register_publisher

class Springer(Publisher):
    """Class for Springer articles"""

    domains = ["link.springer.com","springer.com","www.springer.com"]
    
    def get_title(self):
        """Get article title"""
        self.title = self.soup.find('h1',class_='ArticleTitle').text

    def get_authors(self):
        """Get author given and surnammes"""
        author_raw = self.soup.find_all('span',class_='authors__name')
        self.author_surnames = []
        self.author_givennames = []
        for i in author_raw:
            name = i.text.split('\xa0')
            self.author_surnames.append(name[-1])
            self.author_givennames.append(' '.join(name[:-1]))

    def get_abstract(self):
        """Get article abstract"""
        self.abstract = self.soup.find('section',class_='Abstract')

    def get_keywords(self):
        """Get article keywords"""
        keywords_raw = self.soup.find_all('span',class_='Keyword')
        self.keywords = []
        for i in keywords_raw:
            self.keywords.append(i.text.replace('\xa0',''))

    def get_metadata(self):
        """Get assortment of other metadata"""
        if self.doi == None:
            doi_raw = self.soup.find('span',{"id":"doi-url"}).text.split('/')
            self.doi = doi_raw[-2]+'/'+doi_raw[-1]

        self.journal = self.soup.find('span',class_="JournalTitle").text

        self.year = self.soup.find('time')['datetime'].split('-')[0]

        self.volume = self.soup.find('span',class_="ArticleCitation_Volume") \
            .text[:-2].split(' ')[-1]

        self.pages = self.soup.find('span',class_="ArticleCitation_Pages") \
            .text.split(' ')[-1]

    def get_body(self):
        """Get body of article"""
        self.body = self.soup.find('div',{"id":"body"})

    def get_references(self):
        """Get references list"""
        self.references = self.soup.find('section',{"id":"Bib1"})

register_publisher(Springer)
