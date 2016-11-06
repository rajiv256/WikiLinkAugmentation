import  wikipedia as wi
from bs4 import BeautifulSoup as bs

def process(title) :
    ny = wi.WikipediaPage(title)
    s = ny.html()
    s = s.encode('utf8')
    soup = bs(s, 'lxml')
    return soup
def summary_links(title) :
    soup = process(title)
    part = soup.div
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
            print s
            if ('<p>' in s) :
                k = bs(s,'lxml')
                links += k('a')
            part = part.next_sibling
    return links


table = summary_links('New York')

#.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
print len(table)