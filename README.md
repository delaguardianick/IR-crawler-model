# CPS842-assignment2

- Invert.py generates postingList and dictionary (not used for assignment 2)

- Search.py implements the vector space model for finding similarity between the documents and the query
	- It takes about 47 seconds to generate an ordered list of relevant documents for each query
		- That time is mostly allocated to the calculation of similarity between all the documents vectors and the query vector
			 - Can be optimized further but unsure how to and don't have the time.
	
How to run:
	- If you only want to search 1 query in the collection, or want to use search externally:
		- run: 
		setup()
		search("") to ask for a query through the command line
		or
		setup()
		search("Query we want to search for")
		
		- Returns the list of ALL relevant results to the query according to the IR

	-Else if we want an interface, simply run interface()
		- This will also print the top-K documents along with the titles and authors

- Eval.py evaluates the results of search.py
	- Goes through query.text. For each query, search it up - returning a ranking list
	- Compare that ranking list with the ranking (for the same query) in q rels
	- Return MAP and average R-precision
	
	- Since each individual query takes about 47 seconds to run (due to the dot product mostly)
		- And query.text has 64 queries..
		- eval takes about 50 minutes to finish executing.

How to run:
	eval()

	
