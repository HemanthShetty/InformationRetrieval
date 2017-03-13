# InformationRetrieval
Project Worked on as a part of the information retrieval course in Northeastern University, Boston

Assignment-1
1)General and Focused crawling using Breadth First Search- WebCrawler-BFS.py and Depth First Search- WebCrawler-DFS.py

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


In order to install the python module , we need to use the following commands

python <filename> install
More information regarding installation can be found at https://docs.python.org/2/install/


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



2) WebCrawler-DFS.py
	    Performs the generic crawling behavior specified in Task 1
	    To run generic crawler type the following command in the command line with one argument,
	    python WebCrawler-DFS.py [seedurl]
	    example- python WebCrawler-DFS.py http://en.wikipedia.org/wiki/Sustainable_energy

	    To perform focused crawling specified in Task 2 using DFS type the following command in command line with two arguments,
	    python WebCrawler-DFS.py [seedurl] [keyword]
	    example- python WebCrawler-DFS.py http://en.wikipedia.org/wiki/Sustainable_energy solar

Assignment-2
******************************************************************************************
This assignment is coded using Python version 2.7.10

The program makes use of data.json(data.txt generated by crawler has to be converted to json format and placed in the current working directory) and WT2G_Inlinks file


In order to successfully run this code ,we need following libraries
1) sys
2) re
3) time
the links to download the modules is as follows

1) re : https://pypi.python.org/pypi/re2/#downloads
2) urllib : https://pypi.python.org/pypi/urllib3#downloads
3) BS4 : https://pypi.python.org/pypi/beautifulsoup4/4.3.2


In order to install the python module , we need to use the following commands

python <filename> install
More information regarding installation can be found at https://docs.python.org/2/install/

HOW TO  RUN THE PROGRAM
------------------------
There are is one python file

1) PageRank.py

To perform tasks related to first graph,
   example- python PageRank.py 1A


To perform tasks related to second graph,
   example- python PageRank.py 1B

Uncomment the commented methods to print kendall Tau statistics and store rankings in files




ASSIGNMENT-3
******************************************************************************************

This assignment is coded using Python version 2.7.10

The program makes use of data.json and WT2G_Inlinks file


In order to successfully run this code ,we need following libraries
1) sys
2) re
3) time
3)json
4)os
5) from bs4 import BeautifulSoup

the links to download the modules is as follows

1) re : https://pypi.python.org/pypi/re2/#downloads
2) urllib : https://pypi.python.org/pypi/urllib3#downloads
3) BS4 : https://pypi.python.org/pypi/beautifulsoup4/4.3.2

Running instruction
Run Command- python indexing.py
Uncomment the module you want to run
def main():     #generateCorpus(dataFile)     #unigramIndexer(corpusDirectoryName)     #unigramDocumentStatistics("statistics")     #bigramIndexer(corpusDirectoryName)     #bigramDocumentStatistics("statistics")     #trigramIndexer(corpusDirectoryName)         1)to generate corpus
	uncomment method generateCorpus(dataFile) and run


2) uncomment unigramIndexer(corpusDirectoryName) to generate unigram indexes

3)uncomment bigramIndexer(corpusDirectoryName) to generate bigram indexes

4) uncomment trigramIndexer(corpusDirectoryName) to generate trigram indexes


ASSIGNMENT-4
******************************************************************************************

This assignment is coded using Python version 2.7.10

The program makes use of data.txt(which has the crawled files).
This file must be in the same directory as the python file


In order to successfully run this code ,we need following libraries
1) sys
2) re
3) math
4) operator
5) json
the links to download the modules is as follows

1) BS4 : https://pypi.python.org/pypi/beautifulsoup4/4.3.2



In order to install the python module , we need to use the following commands

python <filename> install
More information regarding installation can be found at https://docs.python.org/2/install/

HOW TO  RUN THE PROGRAM
------------------------
There are two python files which have to be run in order

1)Indexing.py

To create indexing file run following command,
   example- python Indexing.py

Command takes no argument. data.txt which has the raw crawled documents is presumed to be in the same working directory

2)BM25.py

After running Indexing.py an index file called unigramIndex.txt and mapping file called docIDMapping.txt are created in the same directory.   

To get BM25 ranking, run following command,
   example- python BM25.py

a text file known as queries.txt is present in the same working directory. It has the value,
1-global warming potential
2-green power renewable energy
3-solar energy california
4-light bulb bulbs alternative alternatives

format-> {queryID}-{Query}
