# CPS842-project

- Invert.py generates postings list (not used for assignment 2) (Assignment 1)
	- Returns postings

- Search.py implements the vector space model for finding similarity between the documents and the query (Assignment 2)
	- Returns ranking

- Scraper.py has a seed (initial website to be scraped) - Current seed set to: DOMZ - Society:Paranormal "https://dmoz-odp.org/Society/Paranormal/"
	- Gets all the relevant links on seed
		- Extracts content (all visible text -content- and valid url anchor tags -oLinks) from these links 
	- Returns list of objects with all websites (sites)
	ex. sites = [obj(site1), obj(site2),...]

- SiteClass.py is the Website class.
	- SiteClass.Website(title= , description=, url=, content=, oLinks=set())
	
- Main.py main() is the driver function
	- Calls all previous modules and gets necessary info
	- Main -> Scraper -> Invert -> Search -> Main
	- Uses library Pickle() to store filled data structures in local (p_load, p_dump)
		- Used to avoid calling Scraper and Invert all the time

How to run:
- in main.py run setup() at least once.
- Then run main() and input the keyword to be searched.
	- Will return a ranking of most relevant results according to the VSM

PS:
- We haven't been able to completely finish this assignment due to a heavy courseload and personal problems.
These are the features still to be done:
- Implement a web interface (don't think its too hard to link these python files to a website with Flask)
- Implement PageRank (even though all outgoing links are collected for every page, we simply do not have time)

	
