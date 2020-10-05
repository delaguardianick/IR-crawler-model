import invert

filepath = '..\cacm.tar\cacm.all'
mainDict, postings = invert.invert(filepath, False, False)
f = open(filepath, 'r')
cacm = f.read()

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
        # 2
        posting = postings[term][0]
        # print (posting)
        # Get all the doc ID's
        keys = posting.keys()
        # For every doc ID
        # Print ID, term frequency and positions
        for key in keys:
            print("\nDoc ID: {}".format(key))
            freq_pos = postings[term][0][key] 
            print("Term Frequency: {}".format(freq_pos[0]))
            for i in range(len(freq_pos)):
                if i != 0:
                    print("Position: {}".format(freq_pos[1]))
                
            
               

pathPostings = "../output/postings.txt"
pathDict = "../output/dictionary.txt"

test()




