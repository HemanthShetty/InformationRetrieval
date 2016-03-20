# InformationRetrieval
Project Worked on as a part of the information retrieval course in Northeastern University, Boston

Assignment-1
1)General and Focused crawling using Breadth First Search- WebCrawler-BFS.py

Task 1: Crawling the documents(General Crawl):
	Start with the following seed URL: http://en.wikipedia.org/wiki/Sustainable_energy; a Wikipedia article about green energy.
	Your crawler has to respect the politeness policy by using a delay of at least one second between your HTTP requests.
	Follow the links with the prefix http://en.wikipedia.org/wiki that lead to articles only (avoid administrative links containing : ). Non-English articles and external links must not be followed.
	Crawl to depth 5. The seed page is the first URL in your frontier and thus counts for depth 1.  
	Stop once you’ve crawled 1000 unique URLs. Keep a list of these URLs in a text file. Also, keep the downloaded documents (raw html, in text format) with their respective URL for future tasks (transformation, indexing, etc.) 
Task 2: Focused Crawling using BFS: 
Your crawler should be able to consume two arguments: a URL and a keyword to be matched against text, anchor text, or text within a URL.  Starting with the same seed in Task 1, crawl to depth 5 at most, using the keyword “solar”. You should return at most 1000 URLS for each of the following:
	Breadth first crawling
	
Note: Relevant links are all links which are not administrative links(containing :) or links to portions of page (containing '#')

INFORMATION RETRIEVAL -ASSIGNMENT 1
******************************************************************************************

This assignment is coded using Python version 2.7.10
This module starts with seed link "http://en.wikipedia.org/wiki/Sustainable_energy"

In order to successfully run this code ,we need following libraries
1) sys 
2) re
3) requests
4) time
5) BS4 
the links to download the modules is as follows

1) re : https://pypi.python.org/pypi/re2/#downloads
2) urllib : https://pypi.python.org/pypi/urllib3#downloads
3) BS4 : https://pypi.python.org/pypi/beautifulsoup4/4.3.2


********************************************************************************************
In order to install the python module , we need to use the following commands

python <filename> install
More information regarding installation can be found at https://docs.python.org/2/install/

********************************************************************************************
HOW TO  RUN THE PROGRAM
------------------------
There are two python files

1) WebCrawler-BFS.py
   Performs the generic crawling behavior specified in Task 1
   To run generic crawler type the following command in the command line with one argument,
   python WebCrawler-BFS.py [seedurl]
   example- python WebCrawler-BFS.py http://en.wikipedia.org/wiki/Sustainable_energy
   
   To perform focused crawling specified in Task 2 using BFS type the following command in command line with two arguments,
   python WebCrawler-BFS.py [seedurl] [keyword]
   example- python WebCrawler-BFS.py http://en.wikipedia.org/wiki/Sustainable_energy solar


