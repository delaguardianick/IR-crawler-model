# Get all the relevant words from the doc
def gatherWords():
    
    filepath = '..\cacm.tar\cacm.all'
    with open(filepath, 'r') as fp:
        line = fp.readline()
        cnt = 1
        while line and cnt < 25:
            if ".I" in line:
                docName = "doc{}.txt".format(cnt)
                newDoc = open(docName, "w+")
                newDoc.write(line)
                line = fp.readline()
                cnt += 1
            else: 
                newDoc.write(line)
                line = fp.readline()
                cnt += 1
 
def checkIndex():
    for i in range(10):
        print()

# gatherWords()

checkIndex()