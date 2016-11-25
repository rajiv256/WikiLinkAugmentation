# coding=utf-8
import wikipedia
import re
from collections import Counter
import operator
import ArticleClass
from variable import *
from categories import *
from ArticlesSimIndex import *
from parser import *
from socket import error as SocketError
import sys,ssl
import errno

def giveRawContent(article):
    print article
    try:
        page = wikipedia.page(article);
    except wikipedia.exceptions.DisambiguationError as e:
        return "NULL"
    except wikipedia.exceptions.PageError as e:
        return "NULL"
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise  # Not error we are looking for
        pass  # Handle error here.
    except ssl.SSLError:
        e = sys.exc_info()[1]
        if e.errno == ssl.SSL_ERROR_EOF:
            # This is almost certainly due to the cherrypy engine
            # 'pinging' the socket to assert it's connectable;
            # the 'ping' isn't SSL.
            return "NULL"
        elif e.errno == ssl.SSL_ERROR_SSL:
            if e.args[1].endswith('http request'):
                # The client is speaking HTTP to an HTTPS server.
                return "NULL"
            elif e.args[1].endswith('unknown protocol'):
                # The client is speaking some non-HTTP protocol.
                # Drop the conn.
                return "NULL"
        raise
    except:
        return "NULL"

    content = page.content;
    summry = page.summary;
    HTML = page.html();
    return (content,HTML,summry);

def givePrunedContent(article,Content):
    content = "NULL"
    if (Content == "NULL") :
        print article
        try:
            page = wikipedia.page(article);
            content = page.content;
        except wikipedia.exceptions.DisambiguationError as e:
            return "NULL"
        except wikipedia.exceptions.PageError as e:
            return "NULL"
        except SocketError as e:
            if e.errno != errno.ECONNRESET:
                raise  # Not error we are looking for
            pass  # Handle error here.
        except ssl.SSLError:
            e = sys.exc_info()[1]
            if e.errno == ssl.SSL_ERROR_EOF:
                # This is almost certainly due to the cherrypy engine
                # 'pinging' the socket to assert it's connectable;
                # the 'ping' isn't SSL.
                return "NULL"
            elif e.errno == ssl.SSL_ERROR_SSL:
                if e.args[1].endswith('http request'):
                    # The client is speaking HTTP to an HTTPS server.
                    return "NULL"
                elif e.args[1].endswith('unknown protocol'):
                    # The client is speaking some non-HTTP protocol.
                    # Drop the conn.
                    return "NULL"
            raise
        except:
            return "NULL"
    else:
        content = Content
    #HTML = page.html();
    # content = content.decode('utf-8').encode('utf-8','xmlcharrefreplace');
    content = content.lower();
    content = re.sub('[!@#$%&()\n=\'\",\.\\+-/{}^]+',' ',content);
    content = re.sub('[0-9]+',' ',content);
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
    words = [w for w in words if w not in stopListBig];
    # print len(words);
    #print words
    content = " ".join(words);
    return (content);

def giveSummary(article,Content):
    content= "NULL"
    if(Content == "NULL"):
        content = "NULL"
        try:
            content = wikipedia.summary(article);
        except wikipedia.exceptions.DisambiguationError as e:
            return "NULL"
        except wikipedia.exceptions.PageError as e:
            return "NULL"
        except SocketError as e:
            if e.errno != errno.ECONNRESET:
                raise  # Not error we are looking for
            pass  # Handle error here.
        except ssl.SSLError:
            e = sys.exc_info()[1]
            if e.errno == ssl.SSL_ERROR_EOF:
                # This is almost certainly due to the cherrypy engine
                # 'pinging' the socket to assert it's connectable;
                # the 'ping' isn't SSL.
                return "NULL"
            elif e.errno == ssl.SSL_ERROR_SSL:
                if e.args[1].endswith('http request'):
                    # The client is speaking HTTP to an HTTPS server.
                    return "NULL"
                elif e.args[1].endswith('unknown protocol'):
                    # The client is speaking some non-HTTP protocol.
                    # Drop the conn.
                    return "NULL"
            raise
        except:
            return "NULL"
    else:
        content = Content
    # content = content.decode('utf-8').encode('utf-8','xmlcharrefreplace');
    content = content.lower();
    content = re.sub('[!@#$%&()\n=\'\",\.\\+-/{}^]+', ' ', content);
    content = re.sub('[0-9]+', ' ', content);
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
    words = [w for w in words if w not in stopListBig];
    # print len(words);
    #print words
    summry = " ".join(words);
    return summry;


def pruneCategories(article):
    title = article.title
    categories = get_categories(title);  # TODO by rajiv
    print categories
    filters = filter(lambda p : (("Articles" in p) or ("articles" in p)) , categories )
    categories = filter(lambda p : p not in filters , categories)
    return categories
    '''
    simDict = {};
    for catgryTitle in categories:
        simDict[catgryTitle] = simArtclCtgry(article,catgryTitle);
        print simDict[catgryTitle]
    sortedList = [(x,y) for (x,y) in sorted(simDict.items(),key= lambda p : p[1],reverse = True )];
    print sortedList
    sortedList = [x for (x,y) in sortedList]
    return sortedList[:];
    '''


def simArtclCtgry(article,catgryTitle):
    print catgryTitle
    catgryArtcl = ArticleClass.Article(catgryTitle)
    if(catgryArtcl.successful == True):
        print "category page successful"
        catgrySimSum = artcatsimilarity(article, catgryArtcl);  # TODO by sahiti
    else:
        print "not going inside"
        try:
            catgryPage = wikipedia.page("category:" + catgryTitle);
            catgryArtclsList = catgryPage.links;
            if "category" in catgryArtclsList:
                catgryArtclsList.remove("category");
            catgrySimSum = 0;
            for catgryArtclName in catgryArtclsList:
                # INITIALIZE THE CLASS AND NAME THE VARIABLE catgry
                catgryArtcl = ArticleClass.Article(catgryArtclName);
                catgrySimSum += artcatsimilarity(article,catgryArtcl); # TODO by sahiti
            catgrySimSum = catgrySimSum / len(catgryArtclsList);
        except:
            return -1;
    return catgrySimSum;

def pruneArticles(article,catgryTitle,thrshld):
    print article
    artclList = getArticles(DEPTH,catgryTitle)[1];     # DONE by hemanth returns subCat & articles
    print "artclList : ", artclList
    artclDict = {};
    for artclTitle in artclList:
        if("Category" in artclTitle):
            artclTitle = artclTitle.split("Category:")[1]
        artcl = ArticleClass.Article(artclTitle);
        artclDict[artcl] = articleSimilarity(article,artcl);
        print artclTitle
        print "ARTICLE SIMILARITY : "
        print artclDict[artcl]
    sortedList = sorted(artclDict.items(),key = lambda p : p[1][1],reverse = True);
    filterList = [(x,(y,z)) for (x,(y,z)) in sortedList if z > thrshld];
    return filterList


def contentSim(target,relarticles):
    artclDict = {};
    for artclTitle in relarticles:
        if ("Category" in artclTitle):
            artclTitle = artclTitle.split("Category:")[1]
        artcl = ArticleClass.Article(artclTitle);
        print artclTitle
        artclDict[artcl] = articleSimilarity(target, artcl);
        #print artclTitle
        #print artclDict[artcl]
    sortedList = sorted(artclDict.items(), key=lambda p: p[1][1], reverse=True);
    #filterList = [(x, (y, z)) for (x, (y, z)) in sortedList if z > thrshld];
    return sortedList

def SummarySim(target,relarticles):
    artclDict = {};
    for artclTitle in relarticles:
        if ("Category" in artclTitle):
            artclTitle = artclTitle.split("Category:")[1]
        artcl = ArticleClass.Article(artclTitle);
        print artclTitle
        artclDict[artcl] = summarysimilarity(target, artcl);
        #print artclTitle
        #print artclDict[artcl]
    sortedList = sorted(artclDict.items(), key=lambda p: p[1], reverse=True);
    #filterList = [(x, (y, z)) for (x, (y, z)) in sortedList if z > thrshld];
    return sortedList



def giveSimArtcls(article,thrshld):
    catgrys = pruneCategories(article);
    print "pruned articles"
    print catgrys

    totalSimList = [];

    for catgry in catgrys:
        totalSimList += pruneArticles(article,catgry,thrshld);
    justnames = map(lambda p : (p[0].title , p[1]) , totalSimList)
    print justnames

    return totalSimList;



def referenceSimilarity(target,allrelarticles):
    simDict = {}
    target = target.lower().split('(')[0][:-1]
    for relarticle in allrelarticles:
        candidate_article = ArticleClass.Article(relarticle)
        if ("Category" in relarticle):
            relarticle = relarticle.split("Category:")[1]
        links = [re.sub('_',' ',x[1].split("/")[-1]).lower() for x in all_links(relarticle)]
        map(lambda p : p.split('(')[0][:-1]  ,links )
        if target in links:
            print "present in links"
            simDict[relarticle] = 1.0       #/len(links);
        else:
            simDict[relarticle] = 0

        #checking in content also
        content = candidate_article.content
        if(target in content):
            simDict[relarticle] = 1.0

    simDict= sorted(simDict.items() , key = lambda p : p[1],reverse =True)
    simDict = dict(simDict)
    return simDict;



def allrelevantarticles(article):
    catgrys = pruneCategories(article);
    print "pruned articles"
    print catgrys
    totalRelList = [];
    for catgry in catgrys:
        artclList = getArticles(DEPTH, catgry)[1];  # DONE by hemanth returns subCat & articles
        totalRelList +=  artclList;
    articles_stored = variable.allTfIdf.keys()
    totalRelList = filter(lambda p : (p in articles_stored) , totalRelList)
    return totalRelList


def hyperlinkSim(target , relarticles):
    artclDict = {};
    for artclTitle in relarticles:
        #print artclTitle
        if ("Category" in artclTitle):
            artclTitle = artclTitle.split("Category:")[1]
        artcl = ArticleClass.Article(artclTitle);
        artclDict[artcl] = hyperlinksimilarity(target, artcl);
    sortedList = sorted(artclDict.items(), key=lambda p: p[1], reverse=True);
    return sortedList


def see_also_or_not(title,candidate):
    links = see_also(title)
    for i in links:
        if(candidate.lower() == i[0].lower()):
            return 1
    return 0
