import pickle

def getResult(inputFile):
    resultDict = {};
    f = open(inputFile,"r");
    while(True):
        string = f.readline();
        if(string == ""):
            break;
        targetArticle = string.strip().split(",");
        relevantCount = int(targetArticle[1]);
        targetArticle = targetArticle[0];
        # print relevantCount,targetArticle;
        suggestions = []
        for i in range(0,relevantCount):
            temp = f.readline().strip().split(",");
            suggestions += [(temp[0],float(temp[1]),int(temp[2]))];
        resultDict[targetArticle] = suggestions;
        # print resultDict
    return resultDict;

def getPrecision(inputFile):
    precDict = {}
    results = getResult(inputFile);
    for key in results.keys():
        precDict[key] = len([x for x in results[key] if x[2] == 1])/float(len(results[key]));
    return precDict;

def getWikiResult(inputFile):
    resultDict = {};
    f = open(inputFile,"r");
    while(True):
        string = f.readline();
        if(string == ""):
            break;
        targetArticle = string.strip().split(",");
        seeAlsoCount = int(targetArticle[1]);
        targetArticle = targetArticle[0];
        # print relevantCount,targetArticle;
        seeAlso = []
        for i in range(0,seeAlsoCount):
            temp = f.readline().strip().split(",");
            seeAlso += [(temp[0],temp[1])];
        resultDict[targetArticle] = seeAlso;
        # print resultDict
    return resultDict;

def getRecall(ourResultFile,wikiResultFile):
    ourResult = getResult(ourResultFile);
    wikiResult = getWikiResult(wikiResultFile);
    recallDict = {}
    for key in ourResult.keys():
        ourSeeAlso = [x[0].lower() for x in ourResult[key]];
        wikiSeeAlso = [x[0].lower() for x in wikiResult[key]];
        # print key,wikiSeeAlso
        recallDict[key] = len(list(set(ourSeeAlso)&set(wikiSeeAlso)))/float(len(wikiSeeAlso));
    return recallDict;

def getFilteredRecall(ourResultFile,wikiResultFile):
    ourResult = getResult(ourResultFile);
    wikiResult = getWikiResult(wikiResultFile);
    documentStored = pickle.load(open("docsStored.pkl","r"));
    recallDict = {}
    for key in ourResult.keys():
        ourSeeAlso = [x[0].lower() for x in ourResult[key]];
        wikiSeeAlso = [x[0].lower() for x in wikiResult[key] if x[0].lower() in documentStored];
        # print key,ourSeeAlso,wikiSeeAlso
        recallDict[key] = len(list(set(ourSeeAlso)&set(wikiSeeAlso)))/float(len(wikiSeeAlso));
    return recallDict;
# def getRecall(inputFile,wikiSeeAlso):


# def givePrecision(inputFile):

t=getRecall("results","wikiSeeAlso")
s=getFilteredRecall("results","wikiSeeAlso")
