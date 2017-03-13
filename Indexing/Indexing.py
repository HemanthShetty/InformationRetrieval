import re
import io,json,os
from bs4 import BeautifulSoup,Comment

visitedURLS=[]
formattedURLS=[]
wikipediaRegex=re.compile('href="(http(s)?://)?(/*)(wiki/.*?)"')
urlPrefixRegex="http(s)?://en.wikipedia.org/"
urlPrefix="https://en.wikipedia.org/"
dataFile="data.txt"
wikipediaReferencesRegex=re.compile('<span class="mw-headline" id="(References|Notes_and_references)"(.*)')
wikipediaBibiliographyRegex=re.compile('<span class="mw-headline" id="Bibliography_of_cited_references"(.*)')
charactersToBeRemovedRegex=re.compile('[!#$\'\"\|\[\]\{\}\(\)\+\-\^\`\~\:\;\?%\/\=][\*\&]+]')
corpusDirectoryName='corpus'
docIDDictionary={}
vocabularySize=0
unigramInvertedIndex={}
unigramTokensCountMapping={}
unigramInvertedIndexFile="Index/unigramIndex.txt"
docIDMappingFile="Index/docIDMapping.txt"
UnigramNumberOfTokensFile="Index/unigramTokenCount.txt"




def getBodyContentOld(htmlDocument):
	soup=BeautifulSoup(htmlDocument,"html.parser")
	ignore_list=['style','script','html','[document]']
	body=''.join(text for text in soup.find_all(text=True)
              if text.parent.name not in ignore_list)
	return body
def getBodyContent(htmlDocument):
    snippedHtmlDocument= re.sub(wikipediaReferencesRegex, "</body></html>", htmlDocument)
    snippedHtmlDocument= re.sub(wikipediaBibiliographyRegex, "</body></html>", snippedHtmlDocument)
    ignore_list=['table','script','img','thead']
    soup=BeautifulSoup(snippedHtmlDocument,"html.parser")
    documentBody=soup.find('div',id="bodyContent")
    documentTitle=soup.find('h1',id="firstHeading")
    navigationalBar=documentBody.select('div[role=navigation]')+documentBody.select('div[id=jump-to-nav]')
    hiddenTags=documentBody.select('div[id=mw-hidden-catlinks]')+documentBody.select('div[role=search]')
    editSection=documentBody.select('span[class=mw-editsection]')
    footerTags=documentBody.select('div[class=printfooter]')
    wikipediaSectionsToDiscard=documentBody.select('div[id=siteSub]')+documentBody.select('span[id=See_also]')
    references=documentBody.select('sup[class=reference]')+documentBody.select('span[id=references]')\
               +documentBody.select('ol[class=references]')+documentBody.select('span[id=References]')
    externalText=documentBody.findAll("a", {"class" : "external text"})+documentBody.select('span[id=External_links]')
    citation=documentBody.select('span[id=Further_reading]')+documentBody.findAll("cite", {"class" : "citation journal"})
    categories=documentBody.select('div[id=mw-normal-catlinks]')
    seeAlsoSection=[]
    if documentBody.find("span",{"id":"See_also"}) is not None:
        seeAlsoSection=documentBody.find("span",{"id":"See_also"}).find_next('ul').findChildren()
    notesSection=documentBody.select('span[id=Notes]')+documentBody.find_all("div",{"class":"hatnote relarticle mainarticle"})
    contentsSection=documentBody.select('div[id=toc]')
    captionSection=documentBody.select('div[class=ThumbCaption]')+documentBody.select('div[class=thumbcaption]')
    galleryTextSection=documentBody.select('div[class=gallerytext]')+documentBody.select('span[id=Gallery]')
    tagsToBeDiscarded=navigationalBar+hiddenTags+editSection+footerTags+wikipediaSectionsToDiscard+references\
                      +externalText+citation+categories+seeAlsoSection+notesSection+contentsSection+captionSection+galleryTextSection
    for tag in documentBody.find_all(ignore_list)+tagsToBeDiscarded:
        if tag in documentBody.find_all():
            tag.replace_with(' ')
    return documentTitle.text+" "+documentBody.text.strip()


def TokenizeArticleContent(textContent):
    textContent = re.sub(charactersToBeRemovedRegex," ", textContent)
    textContent = re.sub("\.\.\."," ", textContent)
    caseFoldedContent=textContent.lower()
    periodPunctuation=re.finditer('[a-zA-Z][\s\t\r\n\f]*\.',caseFoldedContent)
    for stringSnippet in periodPunctuation:
        start=stringSnippet.start()
        end=stringSnippet.end()
        caseFoldedContent=caseFoldedContent[:start]+stringSnippet.group().replace("."," ")+caseFoldedContent[end:]
    periodPunctuationNumberCase=re.finditer('[0-9]\.[\s]*[^0-9]+',caseFoldedContent)
    for stringSnippet in periodPunctuationNumberCase:
          start=stringSnippet.start()
          end=stringSnippet.end()
          caseFoldedContent=caseFoldedContent[:start]+stringSnippet.group().replace("."," ")+caseFoldedContent[end:]
    commaPunctuations=re.finditer('[a-zA-Z][\s\t\r\n\f]*\,',caseFoldedContent)
    for snippet in commaPunctuations:
         start=snippet.start()
         end=snippet.end()
         caseFoldedContent=caseFoldedContent[:start]+snippet.group().replace(","," ")+caseFoldedContent[end:]
    commaPunctuationsNumberCase=re.finditer('[0-9]\,[\s]*[^0-9]+',caseFoldedContent)
    for snippet in commaPunctuationsNumberCase:
          start=snippet.start()
          end=snippet.end()
          caseFoldedContent=caseFoldedContent[:start]+snippet.group().replace(","," ")+caseFoldedContent[end:]
    return caseFoldedContent


def writeArticleContentToFile(formattedPageName,htmlDocumentContent):
    articleContent=getBodyContent(htmlDocumentContent)
    articleContent=TokenizeArticleContent(articleContent)
    file_ = open("corpus/"+formattedPageName+".txt", 'w')
    file_.write(articleContent.encode('ascii','ignore'))
    file_.close()


def formatPageName(pageName):
    articleTitle=pageName[len("wiki/"):]
    underScoresRemoved = articleTitle.replace("_", "")
    formattedTitle=underScoresRemoved.replace("-","")
    return formattedTitle.replace("/","")



def generateCorpus(dataFileName):
    with open(dataFileName) as data_file:
        storedPages = json.load(data_file)
    for pageName in storedPages:
        pageContent=storedPages[pageName].encode('utf-8')
        formattedPageName=formatPageName(pageName)
        formattedURLS.append(formattedPageName)
        writeArticleContentToFile(formattedPageName,pageContent)

def updateUnigramIndexForDocument(documentTermFrequency,documentID):
    for term in documentTermFrequency:
        if unigramInvertedIndex.has_key(term):
            unigramInvertedIndex[term].append((documentID,documentTermFrequency[term]))
        else:
            unigramInvertedIndex[term]=[(documentID,documentTermFrequency[term])]

def generateBigramTokens(tokens):
    bigramTokens=[]
    i=0
    j=1
    while(j<len(tokens)):
            bigramToken=tokens[i]+" "+tokens[j]
            i=i+1
            j=j+1
            bigramTokens.append(bigramToken)
    return bigramTokens

def generateTrigramTokens(tokens):
    bigramTokens=[]
    i=0
    j=1
    k=2
    while(k<len(tokens)):
            bigramToken=tokens[i]+" "+tokens[j]+" "+tokens[k]
            i=i+1
            j=j+1
            k=k+1
            bigramTokens.append(bigramToken)
    return bigramTokens

def bigramIndexer(corpusDirectoryName):
    documentID=0
    for file in os.listdir(corpusDirectoryName):
        if file.endswith(".txt"):
            with open(corpusDirectoryName+"/"+file) as corpusFile:
                documentTermFrequency={}
                tokens=[]
                content = corpusFile.readlines()
                for line in content:
                    textLine=line.strip('\n')
                    lineTokens=textLine.split()
                    if lineTokens:
                        tokens=tokens+lineTokens
                tokens=generateBigramTokens(tokens)
                documentID=documentID+1
                global docIDDictionary
                docIDDictionary[documentID]=file
                documentTermFrequency=generateIndexFromTokens(tokens,documentTermFrequency)
                updateUnigramIndexForDocument(documentTermFrequency,documentID)
                unigramTokensCountMapping[file]=len(tokens)
    StoreDatastructures(docIDMappingFile,docIDDictionary)
    StoreDatastructures("Index/bigramIndex.txt",unigramInvertedIndex)
    StoreDatastructures("Index/bigramTokenCount.txt",unigramTokensCountMapping)

def trigramIndexer(corpusDirectoryName):
    documentID=0
    for file in os.listdir(corpusDirectoryName):
        if file.endswith(".txt"):
            with open(corpusDirectoryName+"/"+file) as corpusFile:
                documentTermFrequency={}
                tokens=[]
                content = corpusFile.readlines()
                for line in content:
                    textLine=line.strip('\n')
                    lineTokens=textLine.split()
                    if lineTokens:
                        tokens=tokens+lineTokens
                tokens=generateTrigramTokens(tokens)
                documentID=documentID+1
                global docIDDictionary
                docIDDictionary[documentID]=file
                documentTermFrequency=generateIndexFromTokens(tokens,documentTermFrequency)
                updateUnigramIndexForDocument(documentTermFrequency,documentID)
                unigramTokensCountMapping[file]=len(tokens)
    StoreDatastructures(docIDMappingFile,docIDDictionary)
    StoreDatastructures("Index/trigramIndex.txt",unigramInvertedIndex)
    StoreDatastructures("Index/trigramTokenCount.txt",unigramTokensCountMapping)

def unigramIndexer(corpusDirectoryName):
    documentID=0
    for file in os.listdir(corpusDirectoryName):
        if file.endswith(".txt"):
            with open(corpusDirectoryName+"/"+file) as corpusFile:
                documentTermFrequency={}
                tokens=[]
                content = corpusFile.readlines()
                for line in content:
                    textLine=line.strip('\n')
                    lineTokens=textLine.split()
                    if lineTokens:
                        tokens=tokens+lineTokens
                documentID=documentID+1
                global docIDDictionary
                docIDDictionary[documentID]=file
                documentTermFrequency=generateIndexFromTokens(tokens,documentTermFrequency)
                updateUnigramIndexForDocument(documentTermFrequency,documentID)
                unigramTokensCountMapping[file]=len(tokens)
    StoreDatastructures(docIDMappingFile,docIDDictionary)
    StoreDatastructures(unigramInvertedIndexFile,unigramInvertedIndex)
    StoreDatastructures(UnigramNumberOfTokensFile,unigramTokensCountMapping)

def StoreDatastructures(fileName,filedata):
    with io.open(fileName, 'w', encoding='utf-8') as file:
        file.write(unicode(json.dumps(filedata)))


def generateIndexFromTokens(tokens,documentTermFrequency):
    for token in tokens:
        if documentTermFrequency.has_key(token):
            documentTermFrequency[token]=documentTermFrequency[token]+1
        else:
            documentTermFrequency[token]=1
    return documentTermFrequency

def createUnigramTermFrequencyTable(foldername,filename):
    storedIndex={}
    termFrequencyTable={}
    with open('Index/'+'unigramIndex.txt') as data_file:
         storedIndex = json.load(data_file)
    for indexTerm in storedIndex:
         for indexValue in storedIndex[indexTerm]:
             if termFrequencyTable.has_key(indexTerm):
                termFrequencyTable[indexTerm]=termFrequencyTable[indexTerm]+indexValue[1]
             else:
                 termFrequencyTable[indexTerm]=indexValue[1]
    writeTermFrequencyToFile(foldername,filename,termFrequencyTable)

def createbigramTermFrequencyTable(foldername,filename):
    storedIndex={}
    termFrequencyTable={}
    with open('Index/'+'bigramIndex.txt') as data_file:
         storedIndex = json.load(data_file)
    for indexTerm in storedIndex:
         for indexValue in storedIndex[indexTerm]:
             if termFrequencyTable.has_key(indexTerm):
                termFrequencyTable[indexTerm]=termFrequencyTable[indexTerm]+indexValue[1]
             else:
                 termFrequencyTable[indexTerm]=indexValue[1]
    writeTermFrequencyToFile(foldername,filename,termFrequencyTable)

def createtrigramTermFrequencyTable(foldername,filename):
    storedIndex={}
    termFrequencyTable={}
    with open('Index/'+'trigramIndex.txt') as data_file:
         storedIndex = json.load(data_file)
    for indexTerm in storedIndex:
         for indexValue in storedIndex[indexTerm]:
             if termFrequencyTable.has_key(indexTerm):
                termFrequencyTable[indexTerm]=termFrequencyTable[indexTerm]+indexValue[1]
             else:
                 termFrequencyTable[indexTerm]=indexValue[1]
    writeTermFrequencyToFile(foldername,filename,termFrequencyTable)

def writeTermFrequencyToFile(folder,fileName,Table):
    file_ = open(folder+"/"+fileName, 'w')
    j=0
    file_x = open("x.txt", 'w')
    file_y = open("y.txt", 'w')
    file_.write("term"+" : "+"tf"+'\n')
    sortedTable=sorted(Table, key=Table.get,reverse=True)
    for item in sortedTable:
          file_.write(item+" : "+str(Table[item])+'\n')
          j=j+1
          file_x.write(str(j)+'\n')
          file_y.write(str(Table[item])+'\n')

    file_.close()
    file_x.close()
    file_y.close()

def writeDocumentFrequencyToFile(folder,fileName,documentFrequencyTable):
    file_ = open(folder+"/"+fileName, 'w')
    file_.write("term"+" | "+"Docid"+" | "+"DF"+'\n')
    sortedKeys=list(documentFrequencyTable.keys())
    sortedKeys.sort()
    for item in sortedKeys:
        docIds=documentFrequencyTable[item][0:len(documentFrequencyTable[item])-1]
        docFrequency=documentFrequencyTable[item][-1]
        file_.write(item+" | "+str(docIds)+" | "+str(docFrequency)+'\n')
    file_.close()


def createUnigramTermDocumentTable(folderName,filename):
    storedIndex={}
    documentFrequencyTable={}
    with open('Index/'+'unigramIndex.txt') as data_file:
         storedIndex = json.load(data_file)
    for indexTerm in storedIndex:
         for indexValue in storedIndex[indexTerm]:
             if documentFrequencyTable.has_key(indexTerm):
                documentFrequencyTable[indexTerm].append(indexValue[0])
             else:
                 documentFrequencyTable[indexTerm]=[indexValue[0]]
         documentFrequencyTable[indexTerm].append((len(storedIndex[indexTerm])))
    writeDocumentFrequencyToFile(folderName,filename,documentFrequencyTable)

def createbigramTermDocumentTable(folderName,filename):
    storedIndex={}
    documentFrequencyTable={}
    with open('Index/'+'bigramIndex.txt') as data_file:
         storedIndex = json.load(data_file)
    for indexTerm in storedIndex:
         for indexValue in storedIndex[indexTerm]:
             if documentFrequencyTable.has_key(indexTerm):
                documentFrequencyTable[indexTerm].append(indexValue[0])
             else:
                 documentFrequencyTable[indexTerm]=[indexValue[0]]
         documentFrequencyTable[indexTerm].append((len(storedIndex[indexTerm])))
    writeDocumentFrequencyToFile(folderName,filename,documentFrequencyTable)

def createtrigramTermDocumentTable(folderName,filename):
    storedIndex={}
    documentFrequencyTable={}
    with open('Index/'+'trigramIndex.txt') as data_file:
         storedIndex = json.load(data_file)
    for indexTerm in storedIndex:
         for indexValue in storedIndex[indexTerm]:
             if documentFrequencyTable.has_key(indexTerm):
                documentFrequencyTable[indexTerm].append(indexValue[0])
             else:
                 documentFrequencyTable[indexTerm]=[indexValue[0]]
         documentFrequencyTable[indexTerm].append((len(storedIndex[indexTerm])))
    writeDocumentFrequencyToFile(folderName,filename,documentFrequencyTable)

def unigramDocumentStatistics(folderName):
    createUnigramTermFrequencyTable(folderName,"UnigramTermFrequency.txt")
    createUnigramTermDocumentTable(folderName,"UnigramDocumentFrequency.txt")

def bigramDocumentStatistics(folderName):
    createbigramTermFrequencyTable(folderName,"bigramTermFrequency.txt")
    createbigramTermDocumentTable(folderName,"bigramDocumentFrequency.txt")

def trigramDocumentStatistics(folderName):
    createtrigramTermFrequencyTable(folderName,"trigramTermFrequency.txt")
    createtrigramTermDocumentTable(folderName,"trigramDocumentFrequency.txt")


def main():
    #generateCorpus(dataFile)
    #unigramIndexer(corpusDirectoryName)
    #unigramDocumentStatistics("statistics")
    #bigramIndexer(corpusDirectoryName)
    #bigramDocumentStatistics("statistics")
    #trigramIndexer(corpusDirectoryName)
    #writecoordinatesToFile('statistics/bigramTermFrequency.txt')
    trigramDocumentStatistics("statistics")




main()



