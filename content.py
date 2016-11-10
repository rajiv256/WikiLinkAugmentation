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

def givePrunedContent(article):
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
    HTML = page.html();
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
    print words
    content = " ".join(words);
    return (content,HTML);

def giveSummary(article):
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
    print words
    summry = " ".join(words);
    return summry;


def pruneCategories(article):
    title = article.title
    categories = get_categories(title);  # TODO by rajiv
    print categories
    simDict = {};
    for catgryTitle in categories:
        simDict[catgryTitle] = simArtclCtgry(article,catgryTitle);
    sortedList = [(x,y) for (x,y) in sorted(simDict.items(),key= lambda p : p[1]  )];
    print sortedList
    return sortedList[:2];

def simArtclCtgry(article,catgryTitle):
    print catgryTitle
    try:
        #catgryPage = wikipedia.page(catgryTitle);
        catgryArtcl = ArticleClass.Article(catgryTitle)
        catgrySimSum = artcatsimilarity(article, catgryArtcl);  # TODO by sahiti
    except:
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
        print "ARTICLE SIMILARITY : "
        print artclDict[artcl]
    sortedList = sorted(artclDict.items(),key=operator.itemgetter(1));
    filterList = [x for (x,y) in sortedList if y > thrshld];
    return filterList;

def giveSimArtcls(article,thrshld):
    catgrys = pruneCategories(article);
    print "pruned articles"
    print catgrys
    totalSimList = [];
    for catgry in catgrys:
        totalSimList += pruneArticles(article,catgry,thrshld);
    return totalSimList;

# t = givePrunedContent("india")
