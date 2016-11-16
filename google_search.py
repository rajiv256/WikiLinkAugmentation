from pyvirtualdisplay import Display
from selenium import webdriver
import selenium
import time
from selenium.webdriver.common.keys import Keys
import variable
import wikipedia
import re
from tfidf import *
# display = Display(visible=0, size=(800, 600))
# display.start()
#
# driver = webdriver.Chrome("/home/mint/chromedriver")
#
# #driver.get('http://www.google.com')
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
# display.stop()

variable.display.start()
def giveArticlesGoogle(target,candidate):

    query = target+","+candidate
    driver = webdriver.Chrome("/home/sahiti/chromedriver")
    driver.get("https://www.google.com/search?q="+query)
    length =  len(driver.find_elements_by_css_selector('h3'))
    results = map(lambda p: p.find_element_by_tag_name("a").get_attribute("href"), driver.find_elements_by_css_selector('h3')[:length-1])

    noWiki = filter(lambda y: (y.find("en.wikipedia.org") == -1 and y.find(".pdf") == -1 and y.find("www.youtube.com") == -1 and y.find("books.google.co") == -1), results)
    # variable.display.stop()
    return noWiki;

def googleSimilarity1(target,candidate):
    tLinks = wikipedia.page(target).links
    cLinks = wikipedia.page(candidate).links
    tLinks.append(target)
    cLinks.append(candidate)

    tLinks = map(lambda p: p.lower(),tLinks)
    cLinks = map(lambda p: p.lower(),cLinks)


    print target,tLinks
    print candidate,cLinks
    htmlLinks = giveArticlesGoogle(target,candidate);
    scr = 0
    driver = webdriver.Chrome("/home/sahiti/chromedriver")
    for link in htmlLinks:
        driver.get(link)
        words = cleanText(driver.find_element_by_tag_name("body").text);
        print words
        st = len(set(tLinks) & set(words))/float(len(tLinks));
        sc = len(set(cLinks) & set(words))/float(len(cLinks));
        scr += st*sc

    return scr/len(htmlLinks)

def googlesimilarity2(target,candidate):
    htmlLinks = giveArticlesGoogle(target, candidate);
    scr = 0
    driver = webdriver.Chrome("/home/sahiti/chromedriver")
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
    words = [w for w in words if w not in variable.stopListBig];
    # print len(words);
    return words

googlesimilarity2("Fibonacci heap" , "Binary heap")


def CVgooglesmilarity(pagecontent,target,candidate):
    pagetfidf = TfIdf(pagecontent)
    DocConceptVector(pagetfidf)
    return pagetfidf[target]*pagetfidf[candidate]
