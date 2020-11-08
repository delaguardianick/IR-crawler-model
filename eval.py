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
queries = {} #Will hold all queries from query.text
# queries[queryNum] = [[W][A][N]]
rels = {} #Holds all rankingslists for each query from qrels.text
# rels["30"] = ['1926', '2486', '2786', '2917']
filepathcacmAll = '..\cacm.tar\cacm.all'
queryRankings = {}

# Goes through query.text, one query at a time
# and saves all queryNum(bers), W (Abstracts), A(uthors), and N into dict(queries)
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
                queries[queryNum] = []
            
            # If .W in line
            if re.match('\.W$', line):
                query= ""
                line = fQ.readline()
                while( (not re.match('\.N$', line)) and (not re.match('\.A$', line))):
                    query += line.strip()
                    query += " "
                    line = fQ.readline()
                queries[queryNum].append([query])
                
            # If .A in line
            if ".A" == line[:2]:
                authors = []
                line = fQ.readline()
                while (".N" != line[:2]):
                    authors.append(line.strip())
                    line = fQ.readline()
                queries[queryNum].append([authors])

            # If .N in line
            if ".N" == line[:2]:
                N = ""
                line = fQ.readline()
                while (not re.match('^\s*$', line)):
                    N += line.strip()
                    line = fQ.readline()
                queries[queryNum].append([N])

            line = fQ.readline()

# Go through qrels.text and save docIDs for each query into rels()
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

# Gets ranking for each query and compares it to the ranking from qrels.text
# Calculates APQ and R-precision for each doc
# Returns MAP and average R-precision over all queries.
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

# Gets the most relevant documents for query
def getQueryRanking(query):
    print (query)
    ret = search.search(query)
    return ret

# Helper function for compareALL()
# Compares a ranking of a query from this IR (ret) with the relevant documents (rel)
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
compareALL()