import wikipedia
import re
from collections import Counter
import operator
from categories import *;
from variable import *;

def givePrunedContent(article):
    print article
    try:
        page = wikipedia.page(article);
    except wikipedia.exceptions.DisambiguationError as e:
        return "NULL"

    content = page.content;
    # content = content.decode('utf-8').encode('ascii','xmlcharrefreplace');
    content = content.lower();
    content = re.sub('[!@#$%&()\n=\'\",.]*','',content);
    content = re.sub('[0-9]*','',content);
    # print content;
    # content = re.sub('\\\u[0-9]*','',content);
    # words = map(str,content.split(" "));
    words = [];
    for w in content.split(" "):
        try:
            words.append(str(w));
        except UnicodeEncodeError:
            pass
        # print str(w);
    # print len(words);
    words = [w for w in words if w not in stopListBig];
    # print len(words);
    content = " ".join(words);
    return content;

def giveSummary(article):
    try:
        summry = wikipedia.summary(article);
    except wikipedia.exceptions.DisambiguationError as e:
        return "NULL"
    content = wikipedia.summary(article);

    content = content.lower();
    content = re.sub('[!@#$%&()\n=\'\",.]*','',content);
    content = re.sub('[0-9]*','',content);

    words = [];
    for w in content.split(" "):
        try:
            words.append(str(w));
        except UnicodeEncodeError:
            pass
    words = [w for w in words if w not in stopListBig];

    summry = " ".join(words);
    return summry;

def pruneCategories(article):
    categories = giveCategories(article.title);  # TODO by rajiv
    simDict = {};
    for catgryTitle in categories:
        simDict[catgryTitle] = simArtclCtgry(article,catgryTitle);
    sortedList = [x for (x,y) in sorted(simDict.items(),key=operator.itemgetter(1))];
    return sortedList[:2];

def simArtclCtgry(article,catgryTitle):
    catgryPage = wikipedia.page("category:"+catgryTitle);
    catgryArtclsList = catgryPage.links;
    if "category" in catgryArtclsList:
        catgryArtclsList.remove("category");
    catgrySimSum = 0;
    for catgryArtclName in catgryArtclsList:
        # INITIALIZE THE CLASS AND NAME THE VARIABLE catgry
        catgryArtcl = Article(catgryArtclName);
        catgrySimSum += artcatsimilarity(article,catgryArtcl); # TODO by sahiti
    return catgrySimSum/len(catgryArtclsList);

def pruneArticles(article,catgryTitle,thrshld):
    artclList = giveArticles(DEPTH,catgryTitle)[1];     # DONE by hemanth returns subCat & articles
    artclDict = {};
    for artclTitle in artclList:
        artcl = Article(artclTitle);
        artclDict[artcl] = similarity(article,artcl);
    sortedList = sorted(artclDict.items(),key=operator.itemgetter(1));
    filterList = [x for (x,y) in sortedList if y > thrshld];
    return filterList;

def giveSimArtcls(article,thrshld):
    catgrys = pruneCategories(article);
    totalSimList = [];
    for catgry in catgrys:
        totalSimList += pruneArticles(article,catgry,thrshld);
    return totalSimList;

# t = givePrunedContent("india")
