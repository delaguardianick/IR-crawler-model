import invert

mainDict, postings = invert.invert('..\cacm.tar\cacm.all', False, False)


def test(pathDict, pathPostings):
    term = ""
    # _dict = open(pathDict, "r")
    # postings = open(pathPostings, "r")
    # _dict = _dict.read()
   
    while(term != "ZZEND"):
        term = input("Term: ")
        # Doc Frequency
        print("Doc Frequency: {}".format(mainDict[term]))
        # 2
        posting = postings[term][0]
        print(postings[term][0][714])
        print (posting)
        keys = posting.keys()
        for key in keys:
            print("Doc ID: {}".format(key))
            freq_pos = postings[term][0][key] 
            print("Term Frequency: {}".format(freq_pos[0]))
            print("Position: {}".format(freq_pos[1]))





    


pathPostings = "../output/postings.txt"
pathDict = "../output/dictionary.txt"

test(pathDict, pathPostings)




