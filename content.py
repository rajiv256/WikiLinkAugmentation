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
    # content = content.decode('utf-8').encode('ascii','xmlcharrefreplace');
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
    # content = content.decode('utf-8').encode('ascii','xmlcharrefreplace');
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
    categories = get_categories(title)[:1];  # TODO by rajiv
    print categories
    filters = filter(lambda p : (("Articles" in p) or ("articles" in p)) , categories )
    categories = filter(lambda p : p not in filters , categories)
    print categories
    simDict = {};
    for catgryTitle in categories:
        simDict[catgryTitle] = simArtclCtgry(article,catgryTitle);
        print simDict[catgryTitle]
    sortedList = [(x,y) for (x,y) in sorted(simDict.items(),key= lambda p : p[1],reverse = True )];
    print sortedList
    sortedList = [x for (x,y) in sortedList]
    return sortedList[:1];



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
    return filterList;

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

# t = givePrunedContent("india")•
def referenceSimilarity(target,allrelarticles):
    simDict = {}
    for relarticle in allrelarticles:
        print "getting links"
        links = [re.sub('_',' ',x[1].split("/")[-1]).lower() for x in all_links(relarticle)]
        if target.lower() in links:
            simDict[target.lower()] = 1.0/len(links);
        else:
            simDict[target.lower()] = 0
    #links = map(lambda p : p.lower() , links)
    # print links
    return simDict;
