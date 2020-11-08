import invert
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
queries = {}
rels = {}
filepathcacmAll = '..\cacm.tar\cacm.all'
queryRankings = {}


# queries[30] = 
# [['Articles on text formatting systems, including "what you see is what youget" systems.  Examples: t/nroff, scribe, bravo.'], ['30. Dean Krafft (text formatters)']]
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
                # print("Q{}".format(queryNum))
                queries[queryNum] = []
                        
            if re.match('\.W$', line):
                query= ""
                line = fQ.readline()
                while( (not re.match('\.N$', line)) and (not re.match('\.A$', line))):
                    query += line.strip()
                    query += " "
                    line = fQ.readline()
                # print("{}".format(query))
                queries[queryNum].append([query])
                
            
            if ".A" == line[:2]:
                authors = []
                line = fQ.readline()
                while (".N" != line[:2]):
                    authors.append(line.strip())
                    line = fQ.readline()
                # print("{}".format(authors))
                queries[queryNum].append([authors])


            if ".N" == line[:2]:
                N = ""
                line = fQ.readline()
                while (not re.match('^\s*$', line)):
                    N += line.strip()
                    line = fQ.readline()
                # print("{}".format(N))
                queries[queryNum].append([N])

            
            line = fQ.readline()
            # print ("Q{}: {} by {}\n N = ".format(queryNum, query, authors, ))
        # print (count)
        # print(queries[30][0][0])

# rels["30"] = 
# ['1926', '2486', '2786', '2917']
def getRels():
    
    with open(pathQrels, 'r') as fQrel:
        line = fQrel.readline()
        Q = "01"
        while line:
            rankList = []
            prev = Q
            while line[:2] == Q:
                docID = line[3:7]
                rankList.append(docID)
                line = fQrel.readline()
    
            rels[Q] = rankList
            Q = line[:2]
            continue
    # print(rels["30"])

# def getRankings():
#     for i in queries:
#         alt = "0" + str(i)
#         if (str(i) in rels) or (alt in rels):
#             query = queries[i][0][0]
#             ret = getQueryRanking(query)
#             queryRankings[i] = ret
#             if str(i) in rels:
#                 rel = rels[str(i)]
#             else:
#                 rel = rels[alt]

#     # return ret, rel

def compareALL():
    map = 0
    avgRPrec = 0
    for i in queries:
        alt = "0" + str(i)
        if (str(i) in rels) or (alt in rels):
            query = queries[i][0][0]
            ret = getQueryRanking(query)
            queryRankings[i] = ret
            if str(i) in rels:
                rel = rels[str(i)]
            else:
                rel = rels[alt]
    
            apq, rPrec = compare(ret, rel)
            map += apq
            print("MAP so far = {}".format(apq/i))
            avgRPrec += rPrec
            print("avgRprec so far = {}".format(rPrec/i))

    avgRPrec = avgRPrec / len(rels)
    map = map / len(rels)
    print (map, avgRPrec)

def getQueryRanking(query):
    print (query)
    ret = search.search(query)
    return ret

def compare(ret, rel):
    matches = 0
    sumPAtK = 0
    K = len(rel)
    ret = ret[:K]
    for i in range(len(ret)):
        for doc in rel:
            if ret[i][0] == int(doc):
                matches += 1
                pAtK = matches / (i+1)
                sumPAtK += pAtK
                # print("{} : P@{} = {}".format(ret[i][0],i+1, pAtK))
    apq = sumPAtK / len(rel)

    rPrecision = matches / len(rel)
    print(apq, rPrecision)
    return apq, rPrecision            

search.setup(filepathcacmAll)
getQueries()
getRels()
# # compare(queries[30][0][0], rels["30"])
# compare(queries[33][0][0], rels["33"])
compareALL()
# print(rels["01"])

# rel = ['0268', '1696', '1892', '2069', '2123', '2297', '2373', '2667', '2862', '2970']
# ret = [(0000, 0.0317), (268, 0.0321), (2123, 0.0329), (2323, 0.0329), (2499, 0.0331), (2470, 0.0333), (2970, 0.0355), (2862, 0.0365), (2911, 0.0366), (2373, 0.0369)]

# print(getAPQ(ret, rel))