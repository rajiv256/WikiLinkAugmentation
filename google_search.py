from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
import socket
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
import urllib2
from bs4 import BeautifulSoup as bsoup
import re

display = Display(visible=0, size=(800, 600))
display.start()
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
#PATH = "/home/sahiti/NLP/Project2/chromedriver"
PATH = "./chromedriver"
def giveArticlesGoogle(target,candidate,n):

    query = target+" , "+candidate
    driver = webdriver.Chrome(PATH)
    print "time1"
    socket.setdefaulttimeout(1000);
    try:
        driver.get("https://www.google.com/search?q="+query)
    except socket.timeout:
	    print "panic exception raised"
	    return [];
    print "time2"
    length = len(driver.find_elements_by_css_selector('h3'))
    results = map(lambda p: p.find_element_by_tag_name("a").get_attribute("href"), driver.find_elements_by_css_selector('h3')[:length-1])
    print len(results);
    for i in range(2,n+1):
        nextPageLink = driver.find_elements_by_id('navcnt')[0].find_elements_by_css_selector('tbody')[0].find_elements_by_css_selector('tr')[0].find_elements_by_css_selector('td')[i].find_element_by_tag_name('a').get_attribute('href');
        print "time3"
	driver.get(nextPageLink)
	print "time4"
        length =  len(driver.find_elements_by_css_selector('h3'))
        results += map(lambda p: p.find_element_by_tag_name("a").get_attribute("href"), driver.find_elements_by_css_selector('h3')[:length-1])
        print len(results);

    noWiki = filter(lambda y: (y.find("wikivisually.com")==-1 and y.find("wikiwand.com")==-1 and y.find("wikipedia.org") == -1 and y.find(".pdf") == -1 and y.find("www.youtube.com") == -1 and y.find("books.google.co") == -1) and y.find(".ppt")==-1 and y.find(".ps")==-1, results)
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
    htmlLinks = htmlLinks[:10];
    # print "HTML Links :", htmlLinks;
    scr = 0
    sqt = 0
    sqc = 0
    driver = webdriver.Chrome(PATH)

    for link in htmlLinks:
	#driver.refresh()
        print "time5"
   	socket.setdefaulttimeout(10) 
	try:
	    driver.get("view-source:"+link)
	except socket.timeout:
	    print "exception raised"
	    #driver.close();
	    driver = webdriver.Chrome(PATH)
	    continue;
	print "time6"
        print link
        
	try:
	    words = cleanText(driver.find_element_by_tag_name("body").text);
        except NoSuchElementException:
	    print "NoSuchElement"
	    continue;

        wordsLen = len(words)
        words = " ".join(words)
        # print words, tLinks;
        # st = len(set(tLinks) & set(words))/float(len(set(tLinks)));
        # sc = len(set(cLinks) & set(words))/float(len(set(cLinks)));
        st = sum([words.count(x) for x in tLinks])
        sc = sum([words.count(x) for x in cLinks])
        # print set(words);
        print link,st,sc
        scr += st*sc
        sqt += st*st
        sqc += sc*sc
    variable.display.stop()
    #driver.close();
    try:
	driver.close()
    except WebDriverException:
	pass;
    if(sqt == 0 or sqc == 0):
        return 0;
    else:
        return scr/math.sqrt(sqt*sqc)
'''
def googlesimilarity2(target,candidate):
    htmlLinks = giveArticlesGoogle(target, candidate);
    scr = 0
    driver = webdriver.Chrome(PATH)
    sim = 0;
    for link in htmlLinks:
        print "time7"
	driver.get(link)
	print "time8"
        words = cleanText(driver.find_element_by_tag_name("body").text);
        words = " ".join(words)
        sim += CVgooglesmilarity(words,target,candidate)
    print sim
'''
def cleanText(content):
    #print content
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

# print googleSimilarity1("Fibonacci heap" , "Iterator" , 2)

def getCandidateSimilarity(target, candidates, n):
    simDict = [];
    for candidate in candidates:
	    simDict += [ (candidate , googleSimilarity1(target, candidate, n) ) ] ;
    simDict = dict ( sorted(simDict , key = lambda p : p [1] ,reverse = True) )
    return simDict;

#candidates = ["Iterator", "Binary heap", "Adaptive heap sort", "Fibonacci prime", "Graph isomorphism", "Dijkstra's algorithm", "Blossom algorithm"];
#candidates = ["Hemachandra"];
#print getCandidateSimilarity("Fibonacci heap", candidates, 2);

def CVgooglesimilarity(pagecontent,target,candidate):
    pagetfidf = TfIdf(pagecontent)
    DocConceptVector(pagetfidf)
    return pagetfidf[target]*pagetfidf[candidate]

## Written by rajiv
def googleSimilarity3(target, candidate, n):
    tLinks = wikipedia.page(target).links
    cLinks = wikipedia.page(candidate).links
    tLinks.append(target)
    cLinks.append(candidate)

    tLinks = map(lambda p: p.lower(), tLinks)
    cLinks = map(lambda p: p.lower(), cLinks)
    #print tLinks

    htmlLinks = giveArticlesGoogle(target, candidate, n);
    htmlLinks = htmlLinks[:10];
    # print "HTML Links :", htmlLinks;
    scr = 0
    sqt = 0
    sqc = 0
    driver = webdriver.Chrome(PATH)

    for link in htmlLinks:
        print link
        try :
            response = urllib2.urlopen(link)
            html_string = response.read()
            soup = bsoup(html_string,"lxml")
            time.sleep(2.5)  # This should be there. Other wise server will raise TOO MANY REQUESTS Error
            text = soup.get_text().encode('ascii','ignore')
            words = re.sub('[^A-Za-z]+', ' ', text).split(' ')
            print words
        except urllib2.HTTPError :
            print "HTTP Error raised. This happens."
            continue ;


        wordsLen = len(words)
        words = " ".join(words)
        st = sum([words.count(x) for x in tLinks])
        sc = sum([words.count(x) for x in cLinks])
        print link, st, sc
        scr += st * sc
        sqt += st * st
        sqc += sc * sc

    if (sqt == 0 or sqc == 0):
        return 0;
    else:
        return scr / math.sqrt(sqt * sqc)


googleSimilarity3('dijkstra\'s algorithm','Bellman-Ford algorithm',2)




'''
###############################################################

inputFo = open("SampleArticles","r");
outputFo = open("GoogleSimilarity2", "a");
i=0;
for line in inputFo:
    print "***************************"+str(i)+"************************"
    i=i+1;
    target, candidate = line.split("$");
    target = target.strip();
    candidate = candidate.strip();
    outputFo.write(target+"$"+candidate+"$"+str(googleSimilarity3(target, candidate,2))+"\n");
    outputFo.flush();
inputFo.close();
outputFo.close();

'''
