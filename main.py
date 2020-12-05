import invert
import scraper
import pickle
import search
maxID = 0

# Uses pickle module to dump data structure onto a local file
def p_dump(filepath, file):
    with open(filepath, "wb") as fp:
        pickle.dump(file, fp)
    fp.close()

# Loads data structure previously stored (dumped)
def p_load(filepath):
    with open(filepath, "rb") as fp:   # Unpickling
        file = pickle.load(fp)
    fp.close()
    return file

# Calls crawl() in scraper.py to scrape websites into list sites and dumps
def scrapeSites():
    global sites
    sites = scraper.crawl()
    p_dump("sitesDump.txt",sites)

# Loads sites and calls invert() in invert.py to generate postings lists
# Dumps generated postings list
def genPostings():
    global maxID
    # Unpickle sites list containing Website objects
    sites = p_load("sitesDump.txt")
    postings = invert.invert(sites, True, True)

    # Pickle postings list
    p_dump("postingsDump.txt", postings)

# Loads postings list and calls main() in search.py
def VSM(q):
    postings = p_load("postingsDump.txt")
    ranking = search.main(postings, q)
    return ranking

# Loads sites and generates proper info based on VSM ranking
def returnRanking(ranking):
    # Get sites again
    with open("sitesDump.txt", "rb") as fp:   # Unpickling
        sites = pickle.load(fp)
    K = 10
    i = 0
    for rank in ranking[:K]:
        i += 1
        print("{}.".format(i))
        sitenum = rank[0]
        site = sites[sitenum]
        print(site.title)
        print(site.url)
        print(ranking[0])
        
# Function to crawl websites and generate postings list
# Diff function to not have to call all the time
def setup():
    print("Scraping sites: ...")
    scrapeSites()
    print("Generating postings list: ...")
    genPostings()

# Used to search for terms once setup is called at least once
def main():
    # setup()
    while (True):
        q = input("Search: ")
        ranking = VSM(q)
        returnRanking(ranking)
    
main()