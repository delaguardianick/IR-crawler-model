import invert
import math
import time

stop = False
stem = False
mainDict = {}
postings = {}
documentsVectors = {}
N = 0

def search(filepath):
    callInvert(filepath)
    query = getQuery()
    start_time = time.time()
    generateDocVectors()
    generateQueryVector(query)
    ranking = mostSimilar()
    ranking_time = (time.time() - start_time)
    print("Ranking list : {}\nTime to generate ranking: %.2f".format(ranking) % (ranking_time))
    start_time = time.time()
    getTitleAndAuthor(ranking)
    author_time = (time.time() - start_time)
    print("Time to generate authors and titles: %.2f" % author_time)
    

def getQuery():
    Q = input("Search: ")
    inputList = Q.split()
    return inputList

def generateQueryVector(query):
    terms = sorted(postings.keys())
    termID = -1
    for term in terms:
        termID += 1
        value = postings[term][0] # Gets value for every term
        docIDs = value.keys()
        for docID in docIDs:
            if "Q" not in documentsVectors:
                initDocVector("Q")
            # print("{} {} = {}".format(term, query, term == query))
            if term.strip() in query:
                documentsVectors["Q"][termID] = documentsVectors["Q"][termID] + 1

        calcWeights("Q",termID,docIDs, value)

def generateDocVectors():
    global N
    N = invert.getNumberOfDocs() 
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
        calcWeights("IDF",termID,docIDs, value)

        # For each docID, get the vector of the doc and update 
        # the proper index (termID) with the term frequency in that doc
        for docID in docIDs:
            if docID not in documentsVectors:
                initDocVector(docID)
            calcWeights(docID, termID, docIDs, value)

            # Query
            # if "Q" not in documentsVectors:
            #     initDocVector("Q")
            # # print("{} {} = {}".format(term, query, term == query))
            # if term.strip() in query:
            #     documentsVectors["Q"][termID] = documentsVectors["Q"][termID] + 1
        
        # calcWeights("Q",termID,docIDs, value)

def calcWeights(docID, termID, docIDs, value):
    # IDFi = log(N/dfi)
    if docID == "IDF":
        # N = invert.getNumberOfDocs() 
        DFi = len(docIDs)
        IDF = calcIDF(N, DFi)
        documentsVectors["IDF"][termID] = IDF
    
    # TF = 1 + log(F) ; W = TF * IDFi
    if docID == "Q":
        # print (documentsVectors["Q"])
        F = documentsVectors["Q"][termID]
        if F != 0:
            TF = 1 + math.log10(F)
            IDFi = documentsVectors["IDF"][termID]
            documentsVectors["Q"][termID] = TF * IDFi

    # TF = 1 + log(F) ; W = TF * IDFi
    if isinstance(docID, int):
        F = value[docID][0]
        TF = 1 + math.log10(F)
        IDFi = documentsVectors["IDF"][termID]
        documentsVectors[docID][termID] = TF * IDFi   

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

def mostSimilar():
    for i in range(1, N):
        sim(i,"Q")

    doc = None
    vect = documentsVectors["sim"]
    ranking = []
    for i in range(len(vect)):
        if vect[i] != 0:
            ranking.append((i, round(vect[i],4)))
            ranking = sorted(ranking, key=lambda x: x[1])

    if ranking == []:
        return ("No results produced, please try a different query.")
    else:
        return ranking[:10]

def sim(docID, Q):
    vDoc = documentsVectors[docID]
    vQ = documentsVectors[Q]
    
    if "sim" not in documentsVectors:
        initSimVector()

    similarity = vectorMultiply(vDoc, vQ)
    documentsVectors["sim"][docID] = similarity

def vectorMultiply(vDoc, vQ):
    # Length of vectors
    lenVDoc = vectorLength(vDoc)
    lenVQ = vectorLength(vQ)

    sum = 0
    for i in range(len(vDoc)):
        sum += vDoc[i] * vQ[i]
    if (lenVDoc * lenVQ) == 0:
        similarity = 0
    else:
        similarity = sum / (lenVDoc * lenVQ)
    return similarity

def initSimVector():
    documentsVectors["sim"] = []
    N = invert.getNumberOfDocs()
    for i in range(N):
        documentsVectors["sim"].append(0)

def vectorLength(vector):
    # sqrt(i^2 + i2^2 + i3^2 ...)
    total = 0
    for weight in vector:
        total += (weight**2)
    length = math.sqrt(total)
    return length

def getTitleAndAuthor(ranking):
    if isinstance(ranking, str):
        pass
    else:
        for tuple in ranking:
            docID = tuple[0]

            # Open file
            index = ".I {}".format(docID)
            f = open(filepath, 'r')
            line = f.readline()
            author = ""
            title = ""
            while line:
                # If line contains docID we want
                if index == line.strip():
                    line = f.readline() #.T
                    line = f.readline() # title

                    # append title if multiline
                    while ((".W" != line[:2]) and (".B" != line[:2])):
                        title += line
                        line = f.readline()

                    while (".A" != line[:2]):
                        line = f.readline()

                    if ".A" == line[:2]:
                        line = f.readline()
                        author = line.strip()
                else:
                    line = f.readline()

            print("Document ID: {}, \nTitle: {}, \nAuthor: {}\n".format(docID, title.strip(), author))

filepath = '..\cacm.tar\cacm.all'
search(filepath)

