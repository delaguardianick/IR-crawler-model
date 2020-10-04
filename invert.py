import time
import string
from nltk.stem.porter import PorterStemmer

start_time = time.time()

# Get all the relevant words from the doc
useStopWords = False
useStemming = False
def invert(filepath, stop, stem):
    global useStopWords
    global useStemming
    useStopWords = stop
    useStemming = stem
    # print(useStemming)
    generateLists(filepath)
    exportDict(mainDict)
    exportPostings(postings)
    print("--- %s seconds ---" % (time.time() - start_time))


def generateLists(filepath):
    with open(filepath, 'r') as fp:
        line = fp.readline()
        cnt = 1
        docID = 0
        pos = 1
        while line:
            # Index
            if ".I" in line:
                docID += 1
                pos = 1

            # Title
            if ".T" in line:
                title = fp.readline()
                # print(title.strip())
                pos = tokenize(title, docID, pos)

            # Abstract
            if ".W" in line:
                abstract = ""
                line = fp.readline()
                while(".B" not in line):
                    abstract += line.strip() + "\n"
                    line = fp.readline()
                # print(abstract)
                pos = tokenize(abstract, docID, pos)

            # Publication Date
            if ".B" in line:
                line = fp.readline()
                date = line[5:]
                pos = tokenize(date, docID, pos)

            # newDoc.write(line)
            line = fp.readline()
            cnt += 1

mainDict =  {}
postings = {}

def tokenize(string, docID, pos):
    tokens = string.split()
    for token in tokens:
        token = preProcess(token)
        # pass if null
        if token == None:
            pass
        addtoDict(token)
        addtoPostings(token, docID, pos)
        pos += 1
    return pos

# Cleans the string - removes punctuation, whitespace etc
# Calls useStemming and stopword functions if True
def preProcess(token):
    foundStopWord = False
    token = token.strip()
    token = token.lower()
    table = str.maketrans('', '', string.punctuation)
    token = token.translate(table)
    if useStopWords:
        token = filterStopWord(token) 
        if token == None:
            foundStopWord = True
    if useStemming and not foundStopWord:
        token = stemWord(token)
    if not foundStopWord:
        return token

# NoneType error
def filterStopWord(token):
    filepath =  "../cacm.tar/common_words"
    with open(filepath, 'r') as fp:
        stop_words = fp.read()
    if token in stop_words:
        return None
    else: 
        return token

# Stemms the term
def stemWord(token):
    porter = PorterStemmer()
    stemmed = porter.stem(token)
    return stemmed

def addtoPostings(term, docID, pos):
    if term in postings:             
            
        # Check if the term has existed in that DocID before. 
        if docID in postings[term][0]: 
            postings[term][0][docID].append(pos) 
            # increment termFreq every time term appears in same doc
            postings[term][0][docID][0] = postings[term][0][docID][0] + 1
                
        else: 
            # add the position to the doc
            postings[term][0][docID] = [1, pos] 

    # If term does not exist in the positional index dictionary  
    # (first encounter). 
    else: 
        # Initialize the list. 
        postings[term] = [] 
        # The postings list is initially empty. 
        postings[term].append({})       
        # Add doc ID, termFreq, and position to the postings list 
        postings[term][0][docID] = [1, pos] 


def addtoDict(term):
    if term in mainDict:
        mainDict[term] += 1
    else:
        mainDict[term] = 1

def exportDict(mainDict):
    docName = "..\output\dictionary.txt"
    newDoc = open(docName, "w+")	               
    # mainDict = (x for x in mainDict if x is not None)
    for key in sorted(mainDict):
        newDoc.write("%s: %s" % (key, mainDict[key]) + "\n")

def exportPostings(postings):
    docName = "..\output\postings.txt"
    newDoc = open(docName, "w+")

    for key in sorted(postings):
        newDoc.write("%s: %s" % (key, postings[key]) + "\n")

invert('..\cacm.tar\cacm.all', False, False)