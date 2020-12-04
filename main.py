import invert
import siteClass
import scraper
import pickle
import search
maxID = 0

def scrapeSites():
    sites = scraper.crawl()
    with open("sitesDump.txt", "wb") as fp:
        pickle.dump(sites, fp)
    fp.close()

def genPostings():
    global maxID
    # Unpickle sites list containing Website objects
    with open("sitesDump.txt", "rb") as fp:   # Unpickling
        sites = pickle.load(fp)
    postings = invert.invert(sites, True, True)
    fp.close()

    # Pickle postings list
    with open("postingsDump.txt", "wb") as fp:
        pickle.dump(postings, fp)
    fp.close()

def VSM():
    with open("postingsDump.txt", "rb") as fp:   # Unpickling
        postings = pickle.load(fp)
    search.main(postings)
    fp.close()


# scrapeSites()
# genPostings()
VSM()