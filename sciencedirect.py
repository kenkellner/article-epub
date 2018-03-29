import sci-scraper-new

class ScienceDirect(SciArticle):
    
    def get_title(self):
        self.title = self.soup.find('span',class_='title-text').text








test.title = test.soup.find('span',class_='title-text').text

author_raw = test.soup.find('div',class_='author-group') \
        .find_all('span',class_='content')
author_list = []

if len(author_raw) == 1:
    test.authors = author_raw[0].text
else:
    for i in author_raw:
        author_list.append(i.text)
    
    test.author_list = author_list
    
    #test.authors = ", ".join(author_list)


