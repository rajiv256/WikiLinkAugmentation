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

from nltk import word_tokenize


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
    #$ & +,:;=?@  # |'<>.^*()%!-
    content = cleanText(content)
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
    summry = cleanText(content)
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


import  urllib2

def referenceSimilarity(target,allrelarticles):
    simDict = {}
    target = target.decode('utf-8').encode('ascii', 'replace').replace('?', " ")
    target = target.lower().split('(')[0]
    if(target[-1] == " " ):
        target = target[:-1]
    for relarticle in allrelarticles:
        candidate_article = ArticleClass.Article(relarticle)
        if ("Category" in relarticle):
            relarticle = relarticle.split("Category:")[1]
        #print all_links(relarticle)
        relarticle_links = [urllib2.unquote(x[1]) for x in all_links(relarticle)]  # converting to string and then comparing
        #relarticle_links = filter(lambda p : ("/wiki/" in p) , relarticle_links)
        #print "printing links"
        #print relarticle_links
        links = [x.split("/wiki/")[1].replace("_"," ").lower() for x in relarticle_links]
        links = [w.decode('utf-8').encode('ascii', 'replace').replace('?', " ") for w in links]
        links = map(lambda p : p.split('(')[0][:-1] if(p.split('(')[0][-1] == " ") else p.split('(')[0] ,links )
        if target.lower() in links:
            simDict[relarticle] = 1.0       #/len(links);
        else:
            simDict[relarticle] = 0

        #checking in content also
        content = candidate_article.content
        if(target.lower() in content):
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

def see_also_or_not(candidate,links):
    #links = see_also(title)
    #print candidate
    #print links

    candidate = candidate.decode('utf-8').encode('ascii', 'replace').replace('?', " ")
    for i in links:
        link = urllib2.unquote(i[1])
        link = link.decode('utf-8').encode('ascii', 'replace').replace('?', " ")
        link = link.split("/wiki/")[1]
        link = link.replace("_"," ").split("(")[0].replace(" ","")
        candidate = candidate.split("(")[0].replace(" ","")
        if(candidate.lower() == link.lower()):
            return 1
    return 0
