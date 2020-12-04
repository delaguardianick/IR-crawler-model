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

# Driver function
# Scrapes initial sites and returns sites as objects
def crawl():
    init_sites()
    get_sites_info()
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
    initSize = len(sites)
    for site in sites[:initSize]:
        i += 1
        soup = get_site(site.url)
        if soup != "":
            # Get outgoing links
            add_oLinks_to_sites(soup, site)
            site.content = get_visible_text(soup, site) 
        else:
            site.content = ""
        content.append(site.content.strip())

    # for site in sites[initSize:]:
    #     soup = get_site(site.url)
    #     if soup != "":
    #         site.content = get_visible_text(soup, site) 
    #     else:
    #         site.content = ""
    
# Gets links in a page
def add_oLinks_to_sites(soup, site):
    # Add to the initial sites
    get_page_links(soup, site)
    # print(list(site.oLinks)[:1])
    # for url in list(site.oLinks)[:1]:
    #     print("Added:")
    #     soup = get_site(url)
    #     if soup != "":
    #         title = soup.find('title')
    #         if title != None:
    #             title = title.get_text().strip()
    #             # print("append {} to sites {}".format(title, url))
    #             sites.append(siteClass.Website(title,"", url))

# BS4 to scrape all anchor tags of a site and store in set
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

# Validates URL is valid
# (To not count invalid links for as external urls)
def validateURL(url):
    valid = validators.url(url)
    if valid:
        return True
    else: 
        return False

# Gets all visible_text in a page using bs4
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

# crawl()