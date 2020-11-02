import invert

stop = False
stem = False
mainDict = {}
postings = {}


def search():
    # Get all terms in postings sorted
    terms = sorted(postings.keys())

    # Counter to track index of term in postings
    termID = -1 
    # for each term in postings
    for term in terms:
        termID += 1
        # Gets value for every term
        value = postings[term][0]

        # Gets all docIDs for every term
        docIDs = value.keys()

        # For each docID, get the vector of the doc and update 
        # the proper index (termID) with the term frequency in that doc
        for docID in docIDs:
            if docID not in documentsVectors:
                initDoc(docID)

            termFreq = value[docID][0]
            documentsVectors[docID][termID] = termFreq

    print(documentsVectors)

documentsVectors = {}

def initDoc(docID):
        terms = postings.keys()
        documentsVectors[docID] = [0] 
        for i in range(len(terms)-1):
            documentsVectors[docID].append(0)

    # print (documentsVectors)


    
def callInvert(filepath):
    global stop
    global stem
    global mainDict
    global postings

    # i1 = input("Remove stop words? (y/n) ")
    # if i1 == "y":
    #     stop = True
    # elif i1 == "n":
    #     stop == False

    # i2 = input("Activate stemming? (y/n) ")
    # if i1 == "y":
    #     stem = True
    # elif i1 == "n":
    #     stem == False

    mainDict, postings = invert.invert(filepath, stop, stem)
    search()

filepath = '..\cacm.tar\cacmREDUCED.all'
callInvert(filepath)
initDoc(1)