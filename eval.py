# import search
import re
# Inputs: query.text, qrels.text
# Go through all queries in query.text
    # For each, get relevant results from the system (search)
    # Compare with qrels.txt
        # Calc MAP and R-precision
# Output: average MAP and R-Precision values over all queries
pathQueries ='..\cacm.tar\query.text'
pathQrels = '..\cacm.tar\qrels.text'

def getQueries():
    with open(pathQueries, 'r') as fQ:
        line = fQ.readline()
        queryNum = 0
        query = ""
        count = 0
        authors = []
        while line:
            # if ".I" in line:
            if re.match('\.I\s\d', line):
                count += 1
                queryNum += 1
                print("Q{}".format(queryNum))
                        
            if re.match('\.W$', line):
                query= ""
                line = fQ.readline()
                while( (not re.match('\.N$', line)) and (not re.match('\.A$', line))):
                    query += line
                    line = fQ.readline()
                print("{}".format(query))
            
            if ".A" == line[:2]:
                authors = []
                line = fQ.readline()
                while (".N" != line[:2]):
                    authors.append(line.strip())
                    line = fQ.readline()
                print("{}".format(authors))

            if ".N" == line[:2]:
                N = ""
                line = fQ.readline()
                while (not re.match('^\s*$', line)):
                    N += line
                    line = fQ.readline()
                # print("{}".format(N))

            
            line = fQ.readline()
            # print ("Q{}: {} by {}\n N = ".format(queryNum, query, authors, ))
        print (count)

def getRels():
    with open(pathQrels, 'r') as fQrel:
        listofLists = [[]]
        line = fQrel.readline()
        Q = "01"
        while line:
            rankList = []
            prev = Q
            while line[:2] == Q:
                docID = line[3:7]
                rankList.append(docID)
                line = fQrel.readline()
    
            if int(Q) != int(prev) + 1 :
                print("{} = {}+1".format(Q,prev))
                # rankList.append([])
                # continue
            listofLists.append(rankList)
            # print("{}: {}".format(Q, rankList))
            Q = line[:2]
            continue
    print(len(listofLists))
    # printRels(listofLists)

def printRels(ls):
    for i in range(len(ls)):
        print("{}: {}".format(i, ls[i]))
# getQueries()
getRels()