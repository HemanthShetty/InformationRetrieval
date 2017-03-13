import sys
import requests
import re
from bs4 import BeautifulSoup
from time import sleep

MAXDEPTH=5
MAXURLCOUNT=1000
visitedURLS=[]
keyWordSpecificPageURLS=[]
wikipediaRegex=re.compile('href="(http(s)?://)?(/*)(wiki/.*?)"')
urlPrefixRegex="http(s)?://en.wikipedia.org/"
urlPrefix="https://en.wikipedia.org/"
documentDataStore={}


def get_body_content(htmlDocument):
	soup=BeautifulSoup(htmlDocument,"html.parser")
	ignore_list=['style','script','html','[document]']
	body=''.join(text for text in soup.find_all(text=True)
              if text.parent.name not in ignore_list)
	return body

def FilterLinks(pageURL,pageLinks):
    validLinks=[]
    for pageLink in pageLinks:
        isPagePortionLink="#" in pageLink
        isAdministrativeLink=":" in pageLink
        isSelfReferencingLink=(pageURL == pageLink)
        isWikipediaMainPage="Main_Page" in pageLink
        inValidLink=isPagePortionLink or isAdministrativeLink or isSelfReferencingLink or isWikipediaMainPage
        if not inValidLink and pageLink not in validLinks:
            validLinks.append(pageLink)
    return validLinks

def GetLinksWithAnchorText(relevantLinks,pageContent):
    linksWithAnchorText=[]
    for relevantLink in relevantLinks:
            hyperLinkMatchRegex="<a[^>]*?href\\s*=\\s*((\'|\")"+'/'+relevantLink+"(.*?)(\'|\"))[^>]*?(?!/)>([\\w\\.\\s]+)</a>"
            anchorTextMatch=re.findall(hyperLinkMatchRegex,pageContent)
            concatenatedanchorTextString=""
            for anchorText in anchorTextMatch:
                concatenatedanchorTextString=concatenatedanchorTextString+" "+anchorText[4]
            linksWithAnchorText.append((concatenatedanchorTextString,relevantLink))
    return linksWithAnchorText

class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def size(self):
         return len(self.items)

def requestPage(resourceURL):
    url=urlPrefix+resourceURL
    htmlDocument = requests.get(url)
    sleep(1)
    return htmlDocument.text;

def GetLinksOnPage(htmlDocumentContent):
    linkURLS=[]
    linksOnPage=re.findall(wikipediaRegex,htmlDocumentContent)
    for links in linksOnPage:
        linkURLS.append(links[3])
    return linkURLS

def FocusedCrawl(frontier,searchKeyWord,currentDepth):

    "FocusedCrawler Implementation Here"
    if currentDepth==MAXDEPTH:
        return
    if len(keyWordSpecificPageURLS)==MAXURLCOUNT:
        return
    if frontier.isEmpty()==True:
        return
    newFrontier=Stack()
    while ((not frontier.isEmpty()) and len(keyWordSpecificPageURLS)<MAXURLCOUNT):
        urlAnchorTextToCrawl=frontier.pop()
        anchorText=urlAnchorTextToCrawl[0]
        urlToCrawl=urlAnchorTextToCrawl[1]
        completeURLToCrawl=urlPrefix+urlToCrawl
        if completeURLToCrawl not in visitedURLS:
            pageContent=requestPage(urlToCrawl)
            allLinks=GetLinksOnPage(pageContent)
            relevantLinks=FilterLinks(urlToCrawl,allLinks)
            bodyText=get_body_content(pageContent)
            relevantLinksWithAnchorText=GetLinksWithAnchorText(relevantLinks,pageContent)
            isKeyWordInContent=searchKeyWord in bodyText.lower()
            isKeyWordInAnchorText=searchKeyWord in anchorText
            isKeyWordInURL=searchKeyWord in urlToCrawl
            isSeedURL=("SeedURLForCrawler"==anchorText)
            visitedURLS.append(completeURLToCrawl)
            if isKeyWordInAnchorText or isKeyWordInContent or isKeyWordInURL or isSeedURL:
                keyWordSpecificPageURLS.append(completeURLToCrawl)
                for relevantLinkWithAnchorText in relevantLinksWithAnchorText:
                    newFrontier.push(relevantLinkWithAnchorText)
            FocusedCrawl(newFrontier,searchKeyWord,currentDepth+1)

    #FocusedCrawl(newFrontier,searchKeyWord,currentDepth+1)



def StoreCrawledURLs(crawledURLList,fileName):
    file_ = open(fileName, 'w')
    file_.write('\n'.join(map(str,crawledURLList)))
    file_.close()


def main(argv):
    """
    Read the seed URL and Keyword from the command line arguments
    """
    startingDepth=1
    seedURLS=Stack()
    if len(argv)==2:
        pageResourceURI=re.sub(urlPrefixRegex, '', argv[0])
        pageURLAnchorText=("SeedURLForCrawler",pageResourceURI)
        seedURLS.push(pageURLAnchorText)
        searchKeyWord=argv[1]
        FocusedCrawl(seedURLS,searchKeyWord,startingDepth)
        StoreCrawledURLs(keyWordSpecificPageURLS,"FocusedDFSURLs.txt")
    else:
        print("Please pass the correct inputs to the program")


main(sys.argv[1:])


# file_ = open('test.txt', 'w')
# file_.write(str(documentData))
# file_.close()


