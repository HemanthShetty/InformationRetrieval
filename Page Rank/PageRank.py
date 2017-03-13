from __future__ import division
import math
import operator
import sys
import json
import re
from collections import OrderedDict


visitedURLS=[]
'''Dictionary that holds the page link with page rank'''
pageRank={}
perplexityValues=[]
wikipediaLinkPrefix="wiki/"
dataFileFromAssignment1="data.json"
wikipediaRegex=re.compile('href="(http(s)?://)?(/*)(wiki/.*?)"')
'''Data Structure that holds the inlinks graph'''
Page_Inlinks_Mapping={}
d=0.85
d2=0.95
sortedTop50Inlinks=[]

def read_from_file(filename):
	page_map={}
	with open(filename) as file_content:
		lines=[line.rstrip() for line in file_content]
		for line in lines:
			page_list=line.split(' ')
			page_map[page_list[0]]=list(set(page_list[1:len(page_list)]))
	return page_map

def computeKendallTau(rankedList1,rankedList2):
    TotalN=0
    Concordant=0
    Discordant=0
    list1=set(rankedList1.keys())
    list2=set(rankedList2.keys())
    xvalues=[]
    yvalues=[]
    for pageName in list1.intersection(list2):
        xvalues.append(rankedList1[pageName])
        yvalues.append(rankedList2[pageName])
    length=len(xvalues)
    for i in range(0,length):
        for j in range(i+1,length):
            x1=xvalues[i]
            y1=yvalues[i]
            x2=xvalues[j]
            y2=yvalues[j]
            if((x2>x1 and y2>y1)or(x2<x1 and y2<y1)):
                    Concordant=Concordant+1
                    TotalN=TotalN+1
            elif((x2>x1 and y2<y1)or(x2<x1 and y2>y1)):
                    Discordant=Discordant+1
                    TotalN=TotalN+1
    tauValue=(Concordant-Discordant)/TotalN
    print("tauvalue is "+ str(tauValue))




def write_wikipedia_inlinks_to_file(fileName):
    file_ = open(fileName,'w')
    for page,inLinksToPage in Page_Inlinks_Mapping.iteritems():
        inlinkswithoutprefix=[link[len(wikipediaLinkPrefix):] for link in inLinksToPage.split(" ")]
        file_.write(page[len(wikipediaLinkPrefix):]+" "+" ".join(inlinkswithoutprefix)+"\n")
    file_.close()

def write_values_for_graph(fileName):
        file_ = open(fileName,'w')
        graphCoordinates={}
        for key,value in Page_Inlinks_Mapping.items():
            count=len(value)
            if count in graphCoordinates.keys():
                graphCoordinates[count]=graphCoordinates[count]+1
            else:
                graphCoordinates[count]=1
        for numberOfPages in graphCoordinates.values():
            numberOfPages=math.log(numberOfPages,2)
            file_.write(" "+str(numberOfPages))
        file_.write("\n")
        for numberOfInlinks in graphCoordinates.keys():
            if numberOfInlinks==0:
                numberOfInlinks=0;
            else:
                numberOfInlinks=math.log(numberOfInlinks,2)
            file_.write(" "+str(numberOfInlinks))
        file_.close()


def write_perplexity_values_to_file(fileName):
    file_ = open(fileName,'w')
    i=0
    for perplexityValue in perplexityValues:
        file_.write("Perplexity value after iteration "+str(i+1)+" is "+str(perplexityValue)+"\n")
        i=i+1
    file_.close()

def write_top50_inlinks_to_file(fileName,pages_inlinkscounts):
    file_ = open(fileName,'w')
    file_.write("DOCUMENT-ID : INLINK COUNT")
    for page,inlinkcount in pages_inlinkscounts.iteritems():
        file_.write('\n'+page+" : "+str(inlinkcount))
    file_.close()


def write_top50_pageranks_to_file(fileName,sortedTop50PageRanks):
    global pageRank
    file_ = open(fileName,'w')
    file_.write("DOCUMENT-ID : PAGE RANK")
    for page,pageRank in sortedTop50PageRanks.iteritems():
        file_.write("\n"+str(page)+" : "+str(pageRank))
    file_.close()


def GetLinksOnPage(htmlDocumentContent):
    linkURLS=[]
    linksOnPage=re.findall(wikipediaRegex,htmlDocumentContent)
    for links in linksOnPage:
        linkURLS.append(links[3])
    return linkURLS

def FilterLinks(pageURL,pageLinks):
    validLinks=[]
    for pageLink in pageLinks:
        isPagePortionLink="#" in pageLink
        isAdministrativeLink=":" in pageLink
        isWikipediaMainPage="Main_Page" in pageLink
        isSelfReferencingLink=(pageURL == pageLink)
        inValidLink=isPagePortionLink or isAdministrativeLink or isWikipediaMainPage or isSelfReferencingLink
        if not inValidLink and pageLink not in validLinks:
            validLinks.append(pageLink)
    return validLinks

def create_inlinks_mapping(pageURL,filteredLinks):
    for link in filteredLinks:
        if link in visitedURLS:
            if Page_Inlinks_Mapping.has_key(link):
                oldValue=Page_Inlinks_Mapping.get(link);
                if  pageURL not in oldValue:
                    Page_Inlinks_Mapping[link]=oldValue+" "+pageURL
            else:
                Page_Inlinks_Mapping[link]=pageURL

def get_pagerank_values(pagelinks_mapping):
	val_list=[]
	L={}
	Source=[]
	for key,value in pagelinks_mapping.items():
		if not value:
			Source.append(key)
		else:
			val_list+=value
			for v in value:
				if v in L:
					L[v]+=1
				else:
					L[v]=1
	return val_list,L,Source

def set_initial_pagerank(Pages,totalPages):
    for page in Pages:
        pageRank[page]=1.0/totalPages

def get_perplexity(PR):
	entropy=0
	for page in PR:
		p=PR[page]
		entropy+=p*math.log(1/p,2)
	return 2**(entropy)

def get_sinkPR(PR,S):
	sinkPR=0
	for sinkpage in S:
		sinkPR+=PR[sinkpage]
	return sinkPR

def pagerank_after_iteration(P,L,N,S,dvalue):
    newPR={}
    sinkPR=get_sinkPR(pageRank,S);
    for page in P:
		newPR[page]=(1.0-dvalue)/N
		newPR[page]+=dvalue*(sinkPR/N)
		if page in Page_Inlinks_Mapping:
			for q in Page_Inlinks_Mapping[page]:
			    newPR[page]+=dvalue*pageRank[q]/L[q]
    for page in P:
		pageRank[page]=newPR[page]

def compute_pagerank(P,L,N,S,dvalue):
    prev_perplexity=get_perplexity(pageRank)
    perplexity_count=0
    while (perplexity_count<4):
        pagerank_after_iteration(P,L,N,S,dvalue)
        curr_perplexity=get_perplexity(pageRank)
        if math.fabs(curr_perplexity-prev_perplexity) <  1:
            perplexity_count=perplexity_count+1
        else:
            perplexity_count=0
        prev_perplexity=curr_perplexity
        perplexityValues.append(curr_perplexity)

def computeKendallTauPageRankVSInlinks(sortedTop50PageRanks,sortedTop50Inlinks):
            rankedList1=dict(sortedTop50PageRanks)
            rankedList2=dict(sortedTop50Inlinks)
            computeKendallTau(rankedList1,rankedList2)

def computeKendallTau85VS95WG1(sortedTop50PageRanks,P,L,N,Sink,dvalue):
    rankedList1=dict(sortedTop50PageRanks)
    global pageRank
    pageRank={}
    set_initial_pagerank(P,N)
    compute_pagerank(P,L,N,Sink,dvalue)
    sortedTop50PageRanks95 = OrderedDict(sorted(pageRank.items(), key=lambda x: x[1],reverse=True)[:50])
    sortedTop50PageRanks95 = dict((k[len(wikipediaLinkPrefix):],v) for k,v in sortedTop50PageRanks95.iteritems())
    print("Kendall Tau .85 vs .95\n")
    computeKendallTau(rankedList1,sortedTop50PageRanks95)

def computeKendallTau85VS95WG2(sortedTop50PageRanks,P,L,N,Sink,dvalue):
    rankedList1=dict(sortedTop50PageRanks)
    global pageRank
    pageRank={}
    set_initial_pagerank(P,N)
    compute_pagerank(P,L,N,Sink,dvalue)
    sortedTop50PageRanks95 = OrderedDict(sorted(pageRank.items(), key=lambda x: x[1],reverse=True)[:50])
    print("Kendall Tau .85 vs .95\n")
    computeKendallTau(rankedList1,sortedTop50PageRanks95)

def computeKendallTau95vsinlinksWG1(sortedTop50inlinks,P,L,N,Sink,dvalue):
    rankedList2=dict(sortedTop50inlinks)
    global pageRank
    pageRank={}
    set_initial_pagerank(P,N)
    compute_pagerank(P,L,N,Sink,dvalue)
    sortedTop50PageRanks95 = OrderedDict(sorted(pageRank.items(), key=lambda x: x[1],reverse=True)[:50])
    sortedTop50PageRanks95 = dict((k[len(wikipediaLinkPrefix):],v) for k,v in sortedTop50PageRanks95.iteritems())
    print("Kendall Tau .95 vs inlinks\n")
    computeKendallTau(sortedTop50PageRanks95,rankedList2)

def computeKendallTau95vsinlinksWG2(sortedTop50inlinks,P,L,N,Sink,dvalue):
    rankedList2=dict(sortedTop50inlinks)
    global pageRank
    pageRank={}
    set_initial_pagerank(P,N)
    compute_pagerank(P,L,N,Sink,dvalue)
    sortedTop50PageRanks95 = OrderedDict(sorted(pageRank.items(), key=lambda x: x[1],reverse=True)[:50])
    print("Kendall Tau .95 vs inlinks\n")
    computeKendallTau(sortedTop50PageRanks95,rankedList2)

def main(argv):
    if argv is not None:
            if argv[0]=="1A":
                print("Executing for Graph WTG1")
                with open(dataFileFromAssignment1) as data_file:
                    storedPages = json.load(data_file)
                for visitedPageURL in storedPages:
                    visitedURLS.append(visitedPageURL)
                for page in storedPages:
                    pageContent=storedPages[page].encode('utf-8')
                    linksOnPage=GetLinksOnPage(pageContent)
                    filteredLinks=FilterLinks(page,linksOnPage)
                    create_inlinks_mapping(page,filteredLinks)
                write_wikipedia_inlinks_to_file("WG1.txt")
                global Page_Inlinks_Mapping
                for page,inlinks in Page_Inlinks_Mapping.iteritems():
                    Page_Inlinks_Mapping[page]=inlinks.split(u" ")
                write_values_for_graph("WG1log-log.txt")
                P=list(Page_Inlinks_Mapping.keys())
                V,L,Source=get_pagerank_values(Page_Inlinks_Mapping)
                Sink=set(P)-set(V)
                outpages=list(set(V)-set(P))
                P=P+outpages
                N=len(P)
                set_initial_pagerank(P,N)
                compute_pagerank(P,L,N,Sink,d)
                sortedTop50PageRanks = OrderedDict(sorted(pageRank.items(), key=lambda x: x[1],reverse=True)[:50])
                sortedTop50PageRanks = dict((k[len(wikipediaLinkPrefix):],v) for k,v in sortedTop50PageRanks.iteritems())
                sortedTop50Inlinks={}
                for key,value in Page_Inlinks_Mapping.items():
		            sortedTop50Inlinks[key[len(wikipediaLinkPrefix):]]=len(value)
                sortedTop50Inlinks=OrderedDict(sorted(sortedTop50Inlinks.items(), key=lambda x: x[1],reverse=True)[:50])
                print("Proportion of pages with no in-links:"+str(len(Source)/N)+"\n")
                print("Proportion of pages with no out-links:"+str(len(Sink)/N)+"\n")
                write_perplexity_values_to_file("WG1-Perplexity.txt")
                write_top50_pageranks_to_file("WG1-TOP 50 pagerank.txt",sortedTop50PageRanks)
                write_top50_inlinks_to_file("WG1-TOP50-inlinks.txt",sortedTop50Inlinks)
                #computeKendallTauPageRankVSInlinks(sortedTop50PageRanks,sortedTop50Inlinks)
                #computeKendallTau85VS95WG1(sortedTop50PageRanks,P,L,N,Sink,d2)
                #computeKendallTau95vsinlinksWG1(sortedTop50Inlinks,P,L,N,Sink,d2)

            elif argv[0]=="1B":
                print("Executing for Graph WTG1")
                '''Store the inlinks info present in the file in a data structure'''
                Page_Inlinks_Mapping=read_from_file("WT2G_Inlinks.txt")
                P=list(Page_Inlinks_Mapping.keys())
                write_values_for_graph("WG2log-log.txt")
                V,L,Source=get_pagerank_values(Page_Inlinks_Mapping)
                Sink=set(P)-set(V)
                outpages=list(set(V)-set(P))
                P=P+outpages
                N=len(P)
                set_initial_pagerank(P,N)
                compute_pagerank(P,L,N,Sink,d)
                sortedTop50PageRanks = OrderedDict(sorted(pageRank.items(), key=lambda x: x[1],reverse=True)[:50])
                sortedTop50Inlinks={}
                for key,value in Page_Inlinks_Mapping.items():
		            sortedTop50Inlinks[key]=len(value)
                sortedTop50Inlinks=OrderedDict(sorted(sortedTop50Inlinks.items(), key=lambda x: x[1],reverse=True)[:50])
                print("Proportion of pages with no in-links:"+str(len(Source)/N)+"\n")
                print("Proportion of pages with no out-links:"+str(len(Sink)/N)+"\n")
                write_perplexity_values_to_file("WG2-Perplexity.txt")
                write_top50_pageranks_to_file("WG2-TOP 50 pagerank.txt",sortedTop50PageRanks)
                write_top50_inlinks_to_file("WG2-TOP50-inlinks.txt",sortedTop50Inlinks)
                #computeKendallTauPageRankVSInlinks(sortedTop50PageRanks,sortedTop50Inlinks)
                #computeKendallTau85VS95WG2(sortedTop50PageRanks,P,L,N,Sink,d2)
                #computeKendallTau95vsinlinksWG2(sortedTop50Inlinks,P,L,N,Sink,d2)

            else:
                print("Enter a valid argument")
    else:
        print("Enter an argument to specify the input file")







main(sys.argv[1:])
