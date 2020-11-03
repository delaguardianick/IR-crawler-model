import invert
import math

stop = False
stem = False
mainDict = {}
postings = {}
documentsVectors = {}

def sim(Doc, Q):
    None


def generateDocVectors():
    terms = sorted(postings.keys()) # Get all terms in postings sorted
    termID = -1  # Counter to track index of term in postings
    N = invert.getNumberOfDocs() #Size of postings array - used for IDF

    # for each term in postings
    for term in terms:
        termID += 1
        value = postings[term][0] # Gets value for every term
        docIDs = value.keys() # Gets all docIDs for every term

        # IDF
        if "IDF" not in documentsVectors:
                initDocVector("IDF")

        DFi = len(docIDs)
        IDF = calcIDF(N, DFi)
        documentsVectors["IDF"][termID] = IDF

        # For each docID, get the vector of the doc and update 
        # the proper index (termID) with the term frequency in that doc
        for docID in docIDs:
            if docID not in documentsVectors:
                initDocVector(docID)

            F = value[docID][0]
            TF = 1 + math.log10(F)
            IDFi = documentsVectors["IDF"][termID]
            documentsVectors[docID][termID] = TF * IDFi

    # print(documentsVectors['IDF'])
    # printVectors()

def printVectors():
    for vector in documentsVectors:
        print ("{} : {}".format(vector, documentsVectors[vector]))

def calcIDF(N, DFi):
    # N = len(postings.keys())
    IDF = math.log10(N / DFi)
    # print ("{} / {} = {}".format(N,DFi,IDF))

    return IDF
    

# Initializes the document vector to the length of postings. 
# All indexes initially 0
def initDocVector(docID):
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
    generateDocVectors()

filepath = '..\cacm.tar\cacmREDUCED.all'
callInvert(filepath)
