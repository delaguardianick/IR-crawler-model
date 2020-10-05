import invert

def test():
    term = ""
    while(term != None):
        # Ask for user to input the term
        term = input("Term: ")
        if (term == "ZZEND"):
            break
        elif (term not in mainDict):
            print("Word not found")

        # Print doc frequency
        else:
            print("Doc Frequency: {}\n".format(mainDict[term]))
            posting = postings[term][0]
            # print (posting)
            # Get all the doc ID's
            keys = posting.keys()

            # For every doc ID
            # Print ID, term frequency and positions
            for key in keys:
                print("Doc ID: {}".format(key))

                # Gets the title and the context of the term
                title, context = getTitleAndContext(key, term)
                print("Doc title: {}".format(title.strip()))

                # Find termfrequency and position
                freq_pos = postings[term][0][key] 
                print("Term Frequency: {}".format(freq_pos[0]))
                for i in range(len(freq_pos)):
                    if i != 0:
                        print("Position: {}".format(freq_pos[i]))

                print("Context: {}".format(context))
                input()

# Read cacm file, find docID and read its title
def getTitleAndContext(docID, term):
    # Open file
    context = ""
    search = ".I {}".format(docID)
    f = open(filepath, 'r')
    line = f.readline()
    title = ""
    while line:
        # If line contains a new index e.i ".I"
        if search in line:
            line = f.readline() #.T
            line = f.readline() # title

            # append title if multiline
            while ((".W" not in line) and (".B" not in line)):
                title += line
                line = f.readline()
                if term in line: #if term is in the title
                    context = line
            # check same docID for term
            while (".I" not in line):
                if term in line:
                    context = line
                line = f.readline()
        else:
            line = f.readline()
    return title, context

filepath = '..\cacm.tar\cacm.all'
mainDict, postings = invert.invert(filepath, False, False)
test()





