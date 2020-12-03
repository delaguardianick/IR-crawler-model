import invert
import siteClass
import scraper
import pickle


def scrapeSites():
    sites = scraper.crawl()
    with open("sitesDump.txt", "wb") as fp:
        pickle.dump(sites, fp)
    fp.close()

def other():
    with open("sitesDump.txt", "rb") as fp:   # Unpickling
        sites = pickle.load(fp)
    invert.invert(sites, False, False)
    fp.close()

# scrapeSites()
other()