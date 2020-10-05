import invert

def test():
    term = ""
    # _dict = open(pathDict, "r")
    # postings = open(pathPostings, "r")
    # _dict = _dict.read()
   
    while(term != "ZZEND"):
        # Ask for user to input the term
        term = input("Term: ")
        # Print doc frequency
        print("Doc Frequency: {}".format(mainDict[term]))
        posting = postings[term][0]
        # print (posting)
        # Get all the doc ID's
        keys = posting.keys()
        # For every doc ID
        # Print ID, term frequency and positions
        for key in keys:
            print("\nDoc ID: {}".format(key))
            # Get title
            title = getTitle(key).strip()
            print("Doc title: {}".format(title))
            freq_pos = postings[term][0][key] 
            print("Term Frequency: {}".format(freq_pos[0]))
            for i in range(len(freq_pos)):
                if i != 0:
                    print("Position: {}".format(freq_pos[i]))

            input()

def getTitle(docID):
    search = ".I {}".format(docID)
    f = open(filepath, 'r')
    line = f.readline()
    title = ""
    while line:
        if search in line:
            line = f.readline() #.T
            line = f.readline() 
            while ((".W" not in line) and (".B" not in line)):
                title += line
                line = f.readline()
        else:
            line = f.readline()
    return title


# def findMissingIndex():
#     index = 0
#     prevIndex = 0
#     f = open(filepath, 'r')
#     line = f.readline()
#     while (line):
#         if ".I" == line[:2]:
#             index = (line[3:])
#             print(index.strip())
#             if int(index) != (int(prevIndex) + 1):
#                 print ("!=")
#             else:
#                 print("==")
#             line = f.readline()
#             prevIndex = index
#         else:
#             line = f.readline()

# pathPostings = "../output/postings.txt"
# pathDict = "../output/dictionary.txt"

filepath = '..\cacm.tar\cacm.all'
mainDict, postings = invert.invert(filepath, False, False)
test()

# findMissingIndex()




