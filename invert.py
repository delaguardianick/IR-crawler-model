import time
import string
from nltk.stem.porter import PorterStemmer

mainDict =  {}
postings = {}
useStopWords = False
useStemming = False
allIDs = []

# Driver function
def invert(filepath, stop, stem):
    start_time = time.time()
    global useStopWords
    global useStemming
    useStopWords = stop
    useStemming = stem
    generateLists(filepath)
    exportDict(mainDict)
    exportPostings(postings)
    print("Time to generate lists: %.2f seconds" % (time.time() - start_time))
    return (mainDict, postings)

# Get all the relevant lines from the doc and calls tokenize on them
def generateLists(filepath):
    with open(filepath, 'r') as fp:
        line = fp.readline()
        cnt = 1
        docID = 0
        pos = 1
        while line:

            # Index, keeps track of docID
            if ".I" == line[:2]:
                docID += 1
                pos = 1
                allIDs.append(docID) #used for search.py (finding N for IDF calculation)

            # Title
            if ".T" == line[:2]:
                title = fp.readline()
                # print(title.strip())
                pos = tokenize(title, docID, pos)

            # Abstract
            if ".W" == line[:2]:
                abstract = ""
                line = fp.readline()
                while(".B" not in line):
                    abstract += line.strip() + "\n"
                    line = fp.readline()
                # print(abstract)
                pos = tokenize(abstract, docID, pos)

            # Publication Date
            if ".B" == line[:2]:
                line = fp.readline()
                date = line[5:]
                date = date.strip().lower()
                addtoDict(date)
                addtoPostings(date, docID, pos)
                pos += 1
               

            line = fp.readline()
            cnt += 1

# Splits lines into tokens, calls preProcess on each token and adds them 
# to the dictionary and postings list
def tokenize(string, docID, pos):
    tokens = string.split()
    for token in tokens:
        token = preProcess(token)
        if token != "" and token != None:
            pass
            addtoDict(token)
            addtoPostings(token, docID, pos)
            pos += 1
    return pos

# Cleans the string - removes punctuation, whitespace etc
# Calls useStemming and stopword functions if True
def preProcess(token):
    token = token.lower().strip()
    table = str.maketrans('', '', string.punctuation)
    token = token.translate(table)
    
    # if useStopWords is True, call function
    if useStopWords:
        token = filterStopWord(token) 
    
    # If useStemming is True and token is not a stop work, stem the word
    if useStemming:
        token = stemWord(token)
    
    # If the token is not a stop word, return the token to be added to lists
    return token

# NoneType error
# Not working currently
def filterStopWord(token):
    filepath =  "../cacm.tar/stopwords.txt"
    with open(filepath, 'r') as fp:
        stop_words = fp.read()
    if token in stop_words:
        token = ""
    return token

# Stemms the term with Porter's stemming algorithm
def stemWord(token):
    porter = PorterStemmer()
    stemmed = porter.stem(token)
    return stemmed

# Adds the term to the postings list
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
        # Add doc ID, term frequency in doc, and position to the postings list 
        postings[term][0][docID] = [1, pos] 

# Adds the term to the dictionary with frequency 1, 
# if already present add 1 to the frequency
def addtoDict(term):
    if term in mainDict:
        mainDict[term] += 1
    else:
        mainDict[term] = 1

# prints the dictionary into the output file dictionary.txt
def exportDict(mainDict):
    docName = "..\output\dictionary.txt"
    newDoc = open(docName, "w+")	          

    # mainDict = (x for x in mainDict if x is not None)
    for key in sorted(mainDict):
        newDoc.write("%s: %s" % (key, mainDict[key]) + "\n")

# prints the postings list into the output file postings.txt
def exportPostings(postings):
    docName = "..\output\postings.txt"
    newDoc = open(docName, "w+")
    for key in sorted(postings):
        newDoc.write("%s: %s" % (key, postings[key]) + "\n")

def getNumberOfDocs():
    return int(max(allIDs))


# invert('..\cacm.tar\cacm.all', False, False)
