import urllib
import urllib3
# import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import csv
import time

http = urllib3.PoolManager()

class Website:
    def __init__(self, title, description, url, content=""):
        self.title = title
        self.description = description
        self.url = url
        self._content = content

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    def function(self):
        print("Title: "+ self.title +"\nDescription: " + self.description + "\nURL = " + self.url)

seed = Website("DOMZ - Society:Paranormal", "Former Open Directory Project", "https://dmoz-odp.org/Society/Paranormal/")
sites = [seed]

def init_sites():
    url = "https://dmoz-odp.org/Society/Paranormal/"
    soup = getSite(url)

    index = 1
    for item in soup.findAll(class_="site-item"):  
        title = ( item.find(class_="site-title").get_text() )
        description = ( item.find(class_="site-descr").get_text() )
        url = ( item.find(class_="title-and-desc").find("a").get("href"))
        
        sitenum = "site" + str(index)
        sitenum = Website(title.strip(), description.strip(), url.strip())
        sites.append(sitenum)

def getSite(url):
    tic = time.perf_counter()
    
        r = http.request("GET", url)
    toc = time.perf_counter()
    t_elapsed = toc - tic
    # print(r.data)
    soup = BeautifulSoup(r.data,'lxml')
    return soup 

def getPageText():
    # for site in sites:
    site = sites[1]
    content = []
    soup = getSite(site.url)
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    print(site.title)
    site.content = " ".join(t.strip() for t in visible_texts)
    print(site.content)

    content.append(site.content)

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

init_sites()
getPageText()
# print()
