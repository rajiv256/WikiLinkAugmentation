from pyvirtualdisplay import Display
from selenium import webdriver
import selenium
import time
from selenium.webdriver.common.keys import Keys
import variable
import wikipedia
import re
from tfidf import *
import math
#display = Display(visible=0, size=(800, 600))
#display.start()
#
#driver = webdriver.Firefox("chromedriver")
#
#driver.get('http://www.google.com')
#
# query = raw_input("give the query :")
# driver.get("https://www.google.com/search?q="+query)
#
# results = driver.find_elements_by_css_selector('h3')
# link = results[1].find_element_by_tag_name("a")
# href = link.get_attribute("href")
# driver.get(href)
# page = driver.find_element_by_tag_name("body").text
# print page
#
#display.stop()

variable.display.start()
PATH = "/home/sahiti/NLP/Project2/chromedriver"
def giveArticlesGoogle(target,candidate,n):

    query = target+" "+candidate
    driver = webdriver.Chrome(PATH)
    driver.get("https://www.google.com/search?q="+query)
    length = len(driver.find_elements_by_css_selector('h3'))
    results = map(lambda p: p.find_element_by_tag_name("a").get_attribute("href"), driver.find_elements_by_css_selector('h3')[:length-1])
    print len(results);
    for i in range(2,n+1):
        nextPageLink = driver.find_elements_by_id('navcnt')[0].find_elements_by_css_selector('tbody')[0].find_elements_by_css_selector('tr')[0].find_elements_by_css_selector('td')[i].find_element_by_tag_name('a').get_attribute('href');
        driver.get(nextPageLink)
        length =  len(driver.find_elements_by_css_selector('h3'))
        results += map(lambda p: p.find_element_by_tag_name("a").get_attribute("href"), driver.find_elements_by_css_selector('h3')[:length-1])
        print len(results);

    noWiki = filter(lambda y: (y.find("en.wikipedia.org") == -1 and y.find(".pdf") == -1 and y.find("www.youtube.com") == -1 and y.find("books.google.co") == -1), results)
    print len(noWiki);
    #variable.display.stop()
#    driver.close()
    return noWiki;

def googleSimilarity1(target,candidate,n):
    tLinks = wikipedia.page(target).links
    cLinks = wikipedia.page(candidate).links
    tLinks.append(target)
    cLinks.append(candidate)

    tLinks = map(lambda p: p.lower(),tLinks)
    cLinks = map(lambda p: p.lower(),cLinks)
    print tLinks
    # x=raw_input("hi");

    # print target,tLinks
    # print candidate,cLinks
    htmlLinks = giveArticlesGoogle(target,candidate,n);
    # print "HTML Links :", htmlLinks;
    scr = 0
    sqt = 0
    sqc = 0
    driver = webdriver.Chrome(PATH)
    for link in htmlLinks:
        driver.get(link)
        print link
        words = cleanText(driver.find_element_by_tag_name("body").text);
        # print words
        # x=raw_input("hi");
        wordsLen = len(words);
        words = " ".join(words)
        # print words, tLinks;
        # st = len(set(tLinks) & set(words))/float(len(set(tLinks)));
        # sc = len(set(cLinks) & set(words))/float(len(set(cLinks)));
        st = sum([words.count(x) for x in tLinks]);
        sc = sum([words.count(x) for x in cLinks]);
        # print set(words);
        print link,st,sc;
        scr += st*sc
        sqt += st*st
        sqc += sc*sc
    variable.display.stop()
    driver.close()
    if(sqt == 0 or sqc == 0):
        return 0;
    else:
        return scr/math.sqrt(sqt*sqc)

def googlesimilarity2(target,candidate):
    htmlLinks = giveArticlesGoogle(target, candidate);
    scr = 0
    driver = webdriver.Chrome(PATH)
    sim = 0;
    for link in htmlLinks:
        driver.get(link)
        words = cleanText(driver.find_element_by_tag_name("body").text);
        words = " ".join(words)
        sim += CVgooglesmilarity(words,target,candidate)
    print sim

def cleanText(content):
    # content = content.decode('utf-8').encode('ascii','xmlcharrefreplace');
    content = content.lower();
    content = re.sub('[!@#$%&()\n=+\'\",\.\\+-/\{\}^<>\[\]|?_]+',' ',content);
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
    words = [w for w in words if w not in variable.stopListBig];
    # print len(words);

    return words

googleSimilarity1("Fibonacci heap" , "Binary heap" , 2)


def CVgooglesimilarity(pagecontent,target,candidate):
    pagetfidf = TfIdf(pagecontent)
    DocConceptVector(pagetfidf)
    return pagetfidf[target]*pagetfidf[candidate]


