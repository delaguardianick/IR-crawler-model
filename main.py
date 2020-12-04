import invert
import siteClass
import scraper
import pickle
import search
maxID = 0

def scrapeSites():
    global sites
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

def VSM(q):
    with open("postingsDump.txt", "rb") as fp:   # Unpickling
        postings = pickle.load(fp)
    ranking = search.main(postings, q)
    fp.close()
    return ranking

def returnRanking(ranking):
    # Get sites again
    with open("sitesDump.txt", "rb") as fp:   # Unpickling
        sites = pickle.load(fp)
    K = 10
    # print(len(sites[1:]))
    for rank in ranking[:K]:
        sitenum = rank[0]
        site = sites[sitenum]
        print(site.title)
        print(site.url)

def main():
    print("Scraping sites: ...")
    scrapeSites()
    print("Generating postings list: ...")
    genPostings()
    q = input("Search: ")
    ranking = VSM(q)
    returnRanking(ranking)


# scrapeSites()
# genPostings()
# VSM()
main()