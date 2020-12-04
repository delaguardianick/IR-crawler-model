from os import write
import urllib3
import requests
from urllib.request import urlparse, urljoin
from bs4 import BeautifulSoup
from bs4.element import Comment, Doctype
import validators
import siteClass
import invert
OUTGOING = 5

http = urllib3.PoolManager()

seed = siteClass.Website("DOMZ - Society:Paranormal", "Former Open Directory Project", "https://dmoz-odp.org/Society/Paranormal/")
sites = [seed]

def crawl():
    init_sites()
    # get_oLinks()
    get_sites_info()
    print(len(sites))
    return sites

# The inital seed is any page from the dmoz (might be slightly outdated).
# get the site 
def init_sites():
    url = "https://dmoz-odp.org/Society/Paranormal/"
    soup = get_site(url)

    index = 1
    for item in soup.findAll(class_="site-item"):  
        title = ( item.find(class_="site-title").get_text() )
        description = ( item.find(class_="site-descr").get_text() )
        url = ( item.find(class_="title-and-desc").find("a").get("href"))
        
        sitenum = "site" + str(index)
        sitenum = siteClass.Website(title.strip(), description.strip(), url.strip())
        sites.append(sitenum)

# Get html of site. If page doesnt respond in 5 seconds, timeout
# and call exception
def get_site(url):
    soup = ""
    print("Scraping " + url)
    try:
        r = requests.get(url, timeout=5) 
        text = r.text.encode('ascii', 'ignore').decode('ascii')
        soup = BeautifulSoup(text, 'lxml')
        print("Success")
    except Exception as e: 
        print("Connection Timed Out")
    return soup 
    
# Scrapes all visible text on a page and adds it to each site's object
# If page is invalid, content is set to ""
def get_sites_info():
    content = []
    i=0
    for site in sites:
        i += 1
        print
        soup = get_site(site.url)
        if soup != "":
            # Get outgoing links
            get_page_links(soup, site)
            site.content = get_visible_text(soup, site) 
        else:
            site.content = ""
        content.append(site.content.strip())
    
def get_oLinks():
    # Add to the initial sites
    for site in sites:
        soup = get_site(site.url)
        if soup != "":
            get_page_links(soup, site)
            i = 0
            for url in site.oLinks:
                if (i < 0):
                    i += 1
                    soup = get_site(url)
                    title = soup.find('title')
                    sites.append(siteClass.Website(title,"", url))

def get_page_links(soup, site):
    external_urls = set()
    domain_name = urlparse(site.url).netloc
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue  
        if ((domain_name.split(".")[0] not in href) and ("www.blogger.com" not in href)):
        # external link
            if href not in external_urls and validateURL(href):
                external_urls.add(href)
            continue 
    
    site.oLinks = external_urls
    # print(domain_name.split("."))
    # print(site.oLinks)

def validateURL(url):
    valid = validators.url(url)
    if valid:
        return True
    else: 
        return False

def get_visible_text(soup, site):
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return " ".join(t.strip() for t in visible_texts)

# Filter for text visible on a website
# helper to get_sites_info()
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# init_sites()
# get_sites_info()
# write_CACM()
# print(sites[1].function())
print(crawl())