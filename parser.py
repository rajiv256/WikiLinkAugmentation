import  wikipedia as wi
from bs4 import BeautifulSoup as bs
import time
from socket import error as SocketError
import errno


def smoothing(l) :
    ans = []
    for k in l :
        k = k.encode('utf8')
        lsoup = bs(k,'lxml')
        ans.append((lsoup('a')[0].text.encode('utf8'),lsoup('a')[0]['href']))
    return ans


def process(title) :        #returns xml
    try:
        ny = wi.WikipediaPage(title)
        s = ny.html()
        s = s.encode('utf8')
        soup = bs(s, 'lxml')
        # print soup
        return soup
    except wi.exceptions.DisambiguationError as e:
        return []
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise  # Not error we are looking for
        pass  # Handle error here.


def all_links(title) :   #return links for title
    soup = process(title)
    paragraphs = soup('p')
    links = []
    for k in paragraphs:
        if k is None:
            continue
        k = k.encode('utf8')
        lsoup = bs(k, 'lxml')
        links += lsoup('a')

    return smoothing(links)


def summary_links(title) : #return summary links
    soup = process(title)
    part = soup.find('div')
    links = []
    t = 0
    while t < 100 :
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
    return smoothing(links)

def fill_links(article):
    article.summary_links =  summary_links(article.title)
    article.hyperlinks = all_links(article.title)
    return article;

def see_also(title) :
    soup = process(title)
    part = soup.div
    parts = []
    t = 0
    while (part != None) :
        if (len(str(part))<=10) :
            part = part.next_sibling
            continue
        print part.get_text()
        parts.append(part.get_text())
        if (t >= 1000) :
            break
        t += 1
        part = part.next_sibling
    i = len(parts)-1
    s = ""
    while (i > 0) :
        k = parts[i]

        if ("See also" in k.encode('utf-8')) :
            s = parts[i+1]
            break
        i -= 1
    if (len(s)==0) :
        return []
    names = s.split("\n")
    names = [k.encode('utf-8') for k in names]
    return names

def get_categories(title) :
    try:
        ny = wi.WikipediaPage(title)
        name = ny.categories
        name = [k.encode('utf-8') for k in name]
        return name
    except wi.exceptions.DisambiguationError as e:
        return []
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise  # Not error we are looking for
        pass  # Handle error here.


