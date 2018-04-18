from article_epub.publisher import Publisher, register_publisher
import requests
import subprocess
from bs4 import BeautifulSoup

class NIH(Publisher):
    """Class for NIH NCBI articles"""

    name = "NIH-NCBI"
    domains = ["nih.gov"]

    def soupify(self):
        print('Loading page................',end="",flush=True)
        req = requests.get(self.url,headers={'User-Agent':'Mozilla/5.0'})
        self.soup = BeautifulSoup(req.content,'html.parser')
        print('done')   

    def get_doi(self):
        if self.doi == None:
            try:
                self.doi = self.soup.find('span',class_='doi').find('a').text
            except:
                self.doi = ''

    def extract_data(self):
        print('Extracting data from HTML...',end='',flush=True)
        self.get_doi()
        self.get_metadata()
        self.get_citation()
        print('done')

    def epubify(self):

        all_authors = ''
        for i in range(0,len(self.author_surnames)):
            all_authors += self.author_givennames[i] + ' '
            all_authors += self.author_surnames[i]
            if(i != (len(self.author_surnames) - 1)):
                all_authors += ', '

        self.output = self.author_surnames[0]+'_'+self.year+'.epub'
        output_raw = '/tmp/raw.epub'
        
        pdf_link = self.soup.find('div',class_='format-menu') \
            .find_all('a')[2]['href']
        epub_link = 'http://ncbi.nlm.nih.gov'+str(pdf_link) \
            .replace('pdf','epub') 
        
        print('Generating epub.............',end='',flush=True)
        epub = requests.get(epub_link,headers={'User-Agent':'Mozilla/5.0'})
        with open(output_raw, 'wb') as f:
            f.write(epub.content)
            f.close()
        subprocess.check_output(['ebook-convert',output_raw,self.output,
            '--authors',all_authors])
        print('done')

register_publisher(NIH)
