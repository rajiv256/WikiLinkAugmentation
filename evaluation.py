import pickle

n=5;

def getResult(inputFile,n):
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
        for i in range(0,n):
            temp = f.readline().strip().split(",");
            suggestions += [(temp[0],float(temp[1]),int(temp[2]))];
        for i in range(n,relevantCount):
            temp = f.readline();
        resultDict[targetArticle] = suggestions;
        # print resultDict
    return resultDict;

def getPrecision(inputFile):
    precDict = {}
    results = getResult(inputFile,n);
    for key in results.keys():
        if(len(results[key])==0):
            precDict[key] = 0
        else:
            precDict[key] = float(len([x for x in results[key] if x[2] == 1])) /float(len(results[key]));
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
    ourResult = getResult(ourResultFile,n);
    # print ourResult
    wikiResult = getWikiResult(wikiResultFile);
    recallDict = {}
    # print ourResult.keys();
    for key in ourResult.keys():
        ourSeeAlso = [x[0].lower() for x in ourResult[key]];
        wikiSeeAlso = [x[0].lower() for x in wikiResult[key]];
        # print key,wikiSeeAlso
        if(len(wikiSeeAlso) ==0):
            recallDict[key] = 0
        else:
            recallDict[key] = float(len(list(set(ourSeeAlso)&set(wikiSeeAlso))))/float(len(wikiSeeAlso));
    return recallDict;

def getFilteredRecall(ourResultFile,wikiResultFile):
    ourResult = getResult(ourResultFile,n);
    wikiResult = getWikiResult(wikiResultFile);
    documentStored = pickle.load(open("docsStored.pkl","r"));
    recallDict = {}
    for key in ourResult.keys():
        ourSeeAlso = [x[0].lower() for x in ourResult[key]];
        wikiSeeAlso = [x[0].lower() for x in wikiResult[key] if x[0].lower() in documentStored];
        # print key,ourSeeAlso,wikiSeeAlso
        if (len(wikiSeeAlso) == 0):
            recallDict[key] = 0
        else:
            recallDict[key] = float(len(list(set(ourSeeAlso) & set(wikiSeeAlso)))) / float(len(wikiSeeAlso));
    return recallDict;
# def getRecall(inputFile,wikiSeeAlso):


# def givePrecision(inputFile):
p = getPrecision("suggestions3.txt")
t=getRecall("suggestions3.txt","Actual_See_also")
s=getFilteredRecall("suggestions3.txt","Actual_See_also")
print "article \tPrecision\tRecall\tFilteredRecall";
for key in p.keys():
    print str(key)+"\t"+str(p[key])+"\t"+str(t[key])+"\t"+str(s[key])
# t=getResult("suggestions3.txt",5);
