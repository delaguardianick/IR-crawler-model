# Get all the relevant words from the doc
def gatherWords():
    
    filepath = 'cacm.tar\cacm.all'
    with open(filepath, 'r') as fp:
        line = fp.readline()
        cnt = 1
        while line and cnt < 25:
            if ".I" in line:
                newDoc = open("doc1.txt", "w+")
                newDoc.write(line)
                line = fp.readline()
                cnt += 1
            else: 
                newDoc.write(line)
                line = fp.readline()
                cnt += 1
 
def checkIndex():
    print()

gatherWords()