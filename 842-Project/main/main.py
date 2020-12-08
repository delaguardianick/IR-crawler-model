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
def genPostings(stop, stem):
    global maxID
    # Unpickle sites list containing Website objects
    sites = p_load("sitesDump.txt")
    postings = invert.invert(sites, stop, stem)

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
        print(rank)
        
# Function to crawl websites
# Diff function to not have to call scrapeSites() all the time
def setup():
    print("Scraping sites: ...")
    scrapeSites()
    

# Used to search for terms once setup is called at least once
def main():
    stop = input("Filter stop words? (y/n) ")
    if stop == "y":
        stop = True
    else:
        stop = False
    
    stem = input("Stemming? (y/n) ")
    if stem == "y":
        stem = True
    else:
        stem = False

    print("Generating postings list: ...")
    genPostings(stop, stem)

    while (True):
        q = input("Search: ")
        q = invert.preProcess(q, stop, stem)
        ranking = VSM(q)
        returnRanking(ranking)
    
# main()
setup()
main()