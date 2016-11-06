import  wikipedia as wi
from bs4 import BeautifulSoup as bs

def smoothing(l) :
    ans = []
    for k in l :
        k = k.encode('utf8')
        lsoup = bs(k,'lxml')
        ans.append((lsoup('a')[0].text.encode('utf8'),lsoup('a')[0]['href']))
    return ans


def process(title) :        #returns xml
    ny = wi.WikipediaPage(title)
    s = ny.html()
    s = s.encode('utf8')

    soup = bs(s, 'lxml')
    #print soup
    return soup

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

def Filllinks(article):
    article.summary_links =  summary_links(article.title)
    article.hyperlinks = all_links(article.title)
    return article;





l = summary_links('expert system')
print l , len(l)