import  wikipedia as wi
from bs4 import BeautifulSoup as bs
import time
from socket import error as SocketError
import errno
import variable


def smoothing(l) :
    ans = []
    for k in l :
        k = k.encode('utf-8','ignore')
        lsoup = bs(k,'lxml')
        s = lsoup('a')[0].text.encode('utf-8','ignore').lower()
        #TODO : Remove any link with special characters like \x, [ etc.,
        ans.append((lsoup('a')[0].text.encode('utf-8','ignore').lower(),lsoup('a')[0]['href']))
    return ans


def process(title) :        #returns xml
    #print title
    try:
        #print title
        s =  "NULL"

        if(title in variable.allhtmls.keys()):
            #print "html page found successful"
            s = variable.allhtmls[title]
        else:
            print title
            ny = wi.WikipediaPage(title)
            s = ny.html()
        #print "coming here"
        s = s.encode('utf-8','ignore')
        soup = bs(s, 'lxml')
        #print "PRINTING SOUP"
        return soup
    except wi.exceptions.DisambiguationError as e:
        print "disagbiguation error"
        return "NULL"
    except SocketError as e:
        print "socket error"
        if e.errno != errno.ECONNRESET:
            raise  # Not error we are looking for
        pass  # Handle error here.
    except:
         print "some exception"
         return "NULL"


def all_links(title):   #return links for title
    soup = process(title)
    if(soup == "NULL"):
        return []
    paragraphs = soup('p') + soup('table') + soup('ul')
    links = []
    try:
        for k in paragraphs:
            if k is None:
                continue
            k = k.encode('utf-8','ignore')
            lsoup = bs(k, 'lxml')
            links += lsoup('a')
        return smoothing(links)
    except:
        return []




def summary_links(title) : #return summary links
    soup = process(title)
    if (soup == "NULL"):
        return []
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
    if (soup == "NULL"):
        return []
    h2 = soup.find_all('h2')
    ret = []
    for k in h2 :
        if "See also" in k.get_text() :
            k = k.next_sibling.next_sibling
            while (k.name != 'ul') :
                k = k.next_sibling
            links = k.find_all('li')
            for li in links :
               ret.append((li('a')[0].get_text().encode('utf-8','ignore'),li('a')[0]['href'].encode('utf-8','ignore')))
    return ret

def filter_categories(categories_list) :
    f = open('download_categories', 'r')
    cats = []
    s = f.readline()
    while (True):
        s = f.readline()
        if (len(s) == 0):
            break
        splits = s.split(",")
        ss = splits[1]
        name = ss.split(":")[1]   #[:-1 ] why last letter is removed i don't understand
        name = name[:(len(name) - 1)]
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
        categories = [k.encode('utf-8','ignore') for k in categories]
        return filter_categories(categories) ;
    except wi.exceptions.DisambiguationError as e:
        return []
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise  # Not error we are looking for
        pass  # Handle error here.
    except:
        return "NULL"

print see_also('dijkstra\'s algorithm')





























































































































































































































































































































