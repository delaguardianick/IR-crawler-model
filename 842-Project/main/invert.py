from sys import maxunicode
import time
import string
from nltk.stem.porter import PorterStemmer
import re

mainDict =  {}
postings = {}
useStopWords = False
useStemming = False
allIDs = []


# Driver function
def invert(sites, stop, stem):
    start_time = time.time()
    global useStopWords
    global useStemming
    useStopWords = stop
    useStemming = stem
    generateLists(sites)
    # exportDict(mainDict)
    exportPostings(postings)
    # print(postings)
    print("Time to generate lists: %.2f seconds" % (time.time() - start_time))
    maxID = getNumberOfDocs()
    return (postings)

# Get all the relevant lines from the doc and calls tokenize on them
def generateLists(sites):
    # docID = 0
    for site in sites:
        docID = sites.index(site) #Could be better - O(n)
        title = site.title
        # append description to content
        if site.content != "":
            content = site.content + site.description 
        content = site.content
        url = site.url
        num_oLinks = str(len(site.oLinks))

        allIDs.append(docID) #used for search.py (finding N for IDF calculation)
        tokenize(title, docID)
        tokenize(content, docID)
        # docID += 1

# Splits lines into tokens, calls preProcess on each token and adds them 
# to the dictionary and postings list
def tokenize(string, docID):
    tokens = string.split()
    for token in tokens:
        token = preProcess(token, useStopWords, useStemming)
        if token != "" or token != None:
            pass
            addtoDict(token)
            addtoPostings(token, docID)

# Cleans the string - removes punctuation, whitespace etc
# Calls useStemming and stopword functions if True
def preProcess(token, stop, stem):
    regex = re.compile('\\\w*')
    if regex.match(token):
        token = ""
    else:
        token = token.lower().strip()
        table = str.maketrans('', '', string.punctuation)
        token = token.translate(table)
    
    # if useStopWords is True, call function
    if stop:
        token = filterStopWord(token) 
    
    # If useStemming is True and token is not a stop work, stem the word
    if stem:
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
def addtoPostings(term, docID):
    if term in postings:              

        # Check if the term exists in that DocID . 
        if docID in postings[term][0]: 
            # postings[term][0][docID].append(pos) 

            # increment termFreq every time term appears in same doc
            postings[term][0][docID][0] = postings[term][0][docID][0] + 1
        else: 
            # add the position to the doc
            postings[term][0][docID] = [1] 

    # If term does not exist in the positional index dictionary  
    # (first encounter). 
    else: 
        # Initialize the list. 
        postings[term] = [] 
        # The postings list is initially empty. 
        postings[term].append({})       
        # Add doc ID, term frequency in doc, and position to the postings list 
        postings[term][0][docID] = [1] 

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
    regex = re.compile('\\\w*')
    newDoc.write(str(getNumberOfDocs()) + "\n")
    for key in sorted(postings):
        try:
            newDoc.write("{}:{}\n".format(key, postings[key]))
        except Exception as e:
            pass

def getNumberOfDocs():
    return int(max(allIDs))


# filepath = '..\cacm.tar\crawlerOutput.txt'
# invert(filepath, False, False)
