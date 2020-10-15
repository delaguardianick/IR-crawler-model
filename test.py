import invert
import time

stop = False
stem = False
mainDict = {}
postings = {}

def test(stem):
    term = ""
    while(term != None):
        # Ask for user to input the term
        term = input("Term: ")
        start_time = time.time()

        # Terminate on command
        if (term == "ZZEND"):
            break

        # Stem input
        if (stem):
            term = invert.stemWord(term)

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

                print("Context: {}".format(context.strip()))
                # time it took to search term
                search_time = (time.time() - start_time)
                print("Search time: %.2f seconds" % (search_time))
                input("\nPress any key")

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


def test1(filepath):
    global stop
    global stem
    global mainDict
    global postings

    i1 = input("Remove stop words? (y/n) ")
    if i1 == "y":
        stop = True
    elif i1 == "n":
        stop == False

    i2 = input("Activate stemming? (y/n) ")
    if i1 == "y":
        stem = True
    elif i1 == "n":
        stem == False

    mainDict, postings = invert.invert(filepath, stop, stem)
    test(stem)

filepath = '..\cacm.tar\cacm.all'
test1(filepath)
# test()





