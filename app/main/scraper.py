import requests
from xml.etree import ElementTree as et

class Scraper(object):

    def arxiv_scrape(self, link):
        id = link.split('/')
        if id[-1] != "":
            id = id[-1]
        else:
            id = id[-2]
        url = 'http://export.arxiv.org/api/query?id_list=' + id
        xml = requests.get(url).content
        tree = et.fromstring(xml)
        authors = []
        title = ""
        abstract = ""
        for i in range(len(tree)):
            if 'entry' in tree[i].tag:
                for j in range(len(tree[i])):
                    if 'title' in tree[i][j].tag:
                        title = tree[i][j].text
                    elif 'summary' in tree[i][j].tag:
                        abstract = tree[i][j].text
                    if 'author' in tree[i][j].tag:
                        authors.append(tree[i][j][0].text)
        return authors, abstract, title
    
    def get(self, link):
        if 'arxiv' in link:
            authors, abstract, title = self.arxiv_scrape(link)
        #process link
        self.authors = authors
        self.abstract = abstract
        self.title = title
