# Get all the relevant words from the doc



def gatherWords():
    
    filepath = '..\cacm.tar\cacm.all'
    with open(filepath, 'r') as fp:
        line = fp.readline()
        cnt = 1
        docID = 1
        while line and cnt < 400:
            # Index
            if ".I" in line:
                docName = "..\local\doc{}.txt".format(docID)
                newDoc = open(docName, "w+")
                print(docID)
                docID += 1

            # Title
            if ".T" in line:
                title = fp.readline()
                print(title.strip())

            # Abstract
            if ".W" in line:
                abstract = ""
                line = fp.readline()
                while(".B" not in line):
                    abstract += line.strip() + "\n"
                    line = fp.readline()
                print(abstract)

            # Publication Date
            if ".B" in line:
                line = fp.readline()
                date = line[5:]
                print(date.strip())

            newDoc.write(line)
            line = fp.readline()
            cnt += 1

mainDict =  {}
def addtoDict(term, docID):
    None


def preProcessing():
    s = "CACM December, 1958"
    date = s[5:]
    print(date)

gatherWords()

# preProcessing()