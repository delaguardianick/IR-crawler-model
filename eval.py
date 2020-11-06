import search
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
    with open(pathQueries, 'r') as fQu:
        line = fQu.readline()
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
                line = fQu.readline()
                while( (not re.match('\.N$', line)) and (not re.match('\.A$', line))):
                    query += line
                    line = fQu.readline()
                print("{}".format(query))
            
            if ".A" == line[:2]:
                authors = []
                line = fQu.readline()
                while (".N" != line[:2]):
                    authors.append(line.strip())
                    line = fQu.readline()
                print("{}".format(authors))

            if ".N" == line[:2]:
                N = ""
                line = fQu.readline()
                while (not re.match('^\s*$', line)):
                    N += line
                    line = fQu.readline()
                print("{}".format(N))

            # print ("Q{}: {} by {}\n N = ".format(queryNum, query, authors, ))
            line = fQu.readline()
        print (count)
getQueries()