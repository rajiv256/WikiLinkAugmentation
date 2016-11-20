import  wikipedia as wi
from bs4 import BeautifulSoup as bs
import time
from socket import error as SocketError
import errno
import variable


def smoothing(l) :
    ans = []
    for k in l :
        k = k.encode('utf8')
        lsoup = bs(k,'lxml')
        s = lsoup('a')[0].text.encode('utf8').lower()
        #TODO : Remove any link with special characters like \x, [ etc.,
        ans.append((lsoup('a')[0].text.encode('utf8').lower(),lsoup('a')[0]['href']))
    return ans


def process(title) :        #returns xml
    #print title
    try:
        print title
        s =  "NULL"

        if(title in variable.allhtmls.keys()):
            print "html page found successful"
            s = variable.allhtmls[title]
        else:
            ny = wi.WikipediaPage(title)
            s = ny.html()
        #print "coming here"
        s = s.encode('utf-8')
        soup = bs(s, 'lxml')
        #print "PRINTING SOUP"
        return soup
    except wi.exceptions.DisambiguationError as e:
        print "disagbiguation error"
        return []
    except SocketError as e:
        print "socket error"
        if e.errno != errno.ECONNRESET:
            raise  # Not error we are looking for
        pass  # Handle error here.
    # except:
    #
    #     print "some error"
    #     return "NULL"


def all_links(title):   #return links for title
    soup = process(title)
    paragraphs = soup('p') + soup('table') + soup('ul')
    links = []
    try:
        for k in paragraphs:
            if k is None:
                continue
            k = k.encode('utf-8')
            lsoup = bs(k, 'lxml')
            links += lsoup('a')
        return smoothing(links)
    except:
        return []




def summary_links(title) : #return summary links
    soup = process(title)
    part = soup.find('p')
    #print part
    links = []
    t = 0
    #print soup
    try:
        #print soup
        while t < 100 :
            if (part is None) :
                break
            if (len(str(part)) <20) :
                part = part.next_sibling
                continue
            attributes = part.attrs
            if (attributes is None) :
                part = part.next_sibling
                continue
            if (attributes.has_key('id') == True) :
                if (attributes['id'] == 'toc') :
                    break
                else :
                    part = part.next_sibling
            else :
                s = str(part)
                if ('<p>' in s) :
                    k = bs(s,'lxml')
                    links += k('a')
                part = part.next_sibling
        #print links
        return smoothing(links)
    except:
        return []

def fill_links(article):
    # print article.title, "*"*100
    article.summaryhyperlinks =  summary_links(article.title)
    article.hyperlinks = all_links(article.title)
    return article;

def see_also(title) :
    soup = process(title)
    part = soup.div
    parts = []
    t = 0
    try:
        while (part != None) :
            if (len(str(part))<=10) :
                part = part.next_sibling
                continue
            #print part.get_text()
            parts.append(part.get_text())
            if (t >= 1000) :
                break
            t += 1
            part = part.next_sibling
        i = len(parts)-1
        s = ""
        while (i > 0) :
            k = parts[i]
            print k
            if ("See also" in k.encode('utf-8')) :
                s = parts[i+1]
                break
            i -= 1
        if (len(s)==0) :
            return []
        names = s.split("\n")
        names = [k.encode('utf-8') for k in names]
        return names
    except:
        return []

def filter_categories(categories_list) :
    f = open('download_categories', 'r')
    cats = []
    while (True):
        s = f.readline()
        if (len(s) == 0):
            break
        splits = s.split(",")
        ss = splits[1]
        name = ss.split(":")[1][:-1]
        name = str(name)
        name = name.replace("_", " ")
        cats.append(name)
    ret = []
    for k in categories_list :
        if k in cats :
            ret.append(k)
    f.close()
    return ret

def get_categories(title) :
    try:
        ny = wi.WikipediaPage(title)
        categories = ny.categories
        categories = [k.encode('utf-8') for k in categories]
        return filter_categories(categories) ;
    except wi.exceptions.DisambiguationError as e:
        return []
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise  # Not error we are looking for
        pass  # Handle error here.
    except:
        return "NULL"






































































































































































































































































































































