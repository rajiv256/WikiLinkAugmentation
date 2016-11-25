from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
import socket
from pyvirtualdisplay import Display
from selenium import webdriver
import variable
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
import variable
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
    targetVector = []
    candidVector = []
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
	    words = variable.cleanText(driver.find_element_by_tag_name("body").text);
        except NoSuchElementException:
	    print "NoSuchElement"
	    continue;

        # print words, tLinks;
        # st = len(set(tLinks) & set(words))/float(len(set(tLinks)));
        # sc = len(set(cLinks) & set(words))/float(len(set(cLinks)));
        st = sum([words.count(x) for x in tLinks])
        targetVector.append(st);
        sc = sum([words.count(x) for x in cLinks])
        candidVector.append(sc);
        # print set(words);
        # print link,st,sc
        # scr += st*sc
        # sqt += st*st
        # sqc += sc*sc
    variable.display.stop()
    #driver.close();
    try:
	driver.close()
    except WebDriverException:
	pass;
    return vectorSim(targetVector,candidVector);

def vectorSim(tv,cv):
    numerator = 0.0;
    denominator = 0.0;
    xtx = sum([x*x for x in tv]);
    yty = sum([y*y for y in cv]);
    xty = sum([x*y for (x,y) in zip(tv,cv)]);
    return float(xty)/(xtx+yty-xty+0.00001);




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

    #tLinks = map(lambda p: p.lower(), tLinks)
    #cLinks = map(lambda p: p.lower(), cLinks)

    tLinks = map(lambda p: variable.cleanText(p) , tLinks)
    cLinks = map(lambda p: variable.cleanText(p) , cLinks)

    #tLinks = map(lambda p: p.decode('utf-8').encode('ascii', 'replace').replace('?', " "), tLinks)
    #cLinks = map(lambda p: p.decode('utf-8').encode('ascii', 'replace').replace('?', " "), cLinks)

    #print tLinks

    htmlLinks = giveArticlesGoogle(target, candidate, n);
    htmlLinks = htmlLinks[:10];
    # print "HTML Links :", htmlLinks;
    targetVector = []
    candidVector = []
    driver = webdriver.Chrome(PATH)

    for link in htmlLinks:
        #print link
        try :
            response = urllib2.urlopen(link)
            html_string = response.read()
            soup = bsoup(html_string,"lxml")
            time.sleep(2.5)  # This should be there. Other wise server will raise TOO MANY REQUESTS Error
            text = soup.get_text().encode('ascii','ignore')
            text = variable.cleanText(text)
            words = text.split(" ")

            print words
        except urllib2.HTTPError :
            print "HTTP Error raised. This happens."
            continue ;
        except urllib2.URLError :
            print "Error...But Its ok!"
            continue ;


        wordsLen = len(words)
        st = sum([words.count(x) for x in tLinks])
        targetVector.append(st);
        sc = sum([words.count(x) for x in cLinks])
        candidVector.append(sc);
    return vectorSim(targetVector,candidVector);


# t=googleSimilarity3('Double-ended queue','Kinetic priority queue',2)
# print t
# t=googleSimilarity3('Fibonacci Heap','Binomial Heap',2)
'''
def mahalanobisDistance(tv,cv):
    mu = sum([(x+y)/2.0 for (x,y) in zip(tv,cv)]);
    mtv = [x-y for (x,y) in zip(tv,mu)]
    mcv = [x-y for (x,y) in zip(cv,mu)]
    return math.sqrt(sum[((v-w)*(v-w))/(x*y) for ((v,w),(x,y)) in zip(zip(tv,cv),zip(mtv,mcv))]);
'''


'''
##################################################################
'''
'''
inputFo = open("SampleArticles","r");
outputFo = open("GoogleSimilarity4", "a");
i=0;
for line in inputFo:
    print "***************************"+str(i)+"************************"
    i=i+1;
    target, candidate = line.split("$");
    target = target.strip();
    candidate = candidate.strip();
    print target,candidate
    outputFo.write(target+"$"+candidate+"$"+str(googleSimilarity3(target, candidate,2))+"\n");
    outputFo.flush();
inputFo.close();
outputFo.close();
'''


def googlesimilarity_relarticles(target_a , relarticles , depth):
    googlesimilarites = []
    for article in relarticles:
        googlesimilarites[article] = googleSimilarity3(target_a, article, depth)
    return googlesimilarites