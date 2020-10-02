# Get all the relevant words from the doc

def gatherWords():
    filepath = '..\cacm.tar\cacm.all'
    with open(filepath, 'r') as fp:
        line = fp.readline()
        cnt = 1
        docID = 0
        pos = 1
        while line:
            # Index
            if ".I" in line:
                # docName = "..\local\doc{}.txt".format(docID)
                # newDoc = open(docName, "w+")
                # print(docID)
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
        addtoDict(token)
        addtoPostings(token, docID, pos)
        pos += 1
    return pos

def addtoPostings(term, docID, pos):
    if term in postings: 
                          
        # Increment total freq by 1. 
        # postings[term][0] = postings[term][0] + 1
            
        # Check if the term has existed in that DocID before. 
        if docID in postings[term][1]: 
            postings[term][1][docID].append(pos) 
                
        else: 
            postings[term][1][docID] = [pos] 

    # If term does not exist in the positional index dictionary  
    # (first encounter). 
    else: 
        # Initialize the list. 
        postings[term] = [] 
        # The total frequency is 1. 
        postings[term].append(None) 
        # The postings list is initially empty. 
        postings[term].append({})       
        # Add doc ID to postings list. 
        postings[term][1][docID] = [pos] 


def addtoDict(term):
    if term in mainDict:
        mainDict[term] += 1
    else:
        mainDict[term] = 1

def preProcessing():
    s = "CACM December, 1958"
    s = s.split()
    for i in s:
        print(i)

gatherWords()
# print(mainDict)
print("\n")
print(postings)

# preProcessing()