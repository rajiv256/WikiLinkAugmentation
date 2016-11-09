'''
Created on 28-Oct-2016

@author: hemanth
'''
import requests
import json;
#WIKI_API = "http://localhost/mediawiki/api.php";
WIKI_API = "http://en.wikipedia.org/w/api.php";
#'cmtitle':'Category:Machine_learning'
#'cmtitle':'Category:Defunct airports in Prince Edward Island'
# parameters = {'action':'query', 'list':'categorymembers','cmtitle':'Category:Machine learning', 'format':'json', u'cmcontinue': u'page|274545492f414d372b2f4b353745043d2f2749413741330342274545492f414d372b2f4b353745043d2f2749413741330133018f788f7e8f1a|19463198'}
# r = requests.get("http://en.wikipedia.org/w/api.php", params=parameters);
# print r.json()['query']['categorymembers'][0]['title'];

def getArticles(depth, category):
    articleList = [];
    subCat=['Category:'+category];
    idx=0;
    for i in range(depth):
        length = len(subCat);
        while (idx<length):
            catParams = {'action':'query', 'list':'categorymembers','cmtype':'subcat', 'cmtitle':subCat[idx], 'format':'json'}
            jsonResp = requests.get(WIKI_API, catParams).json();
            for catResp in jsonResp['query']['categorymembers']:
                subCat.append(catResp['title']);
            while ('continue' in jsonResp):
                catParams['cmcontinue'] = jsonResp['continue']['cmcontinue'];
                jsonResp = requests.get(WIKI_API, catParams).json();
                if 'query' not in jsonResp or 'categorymembers' not in jsonResp['query']:
                    continue;
                for catResp in jsonResp['query']['categorymembers']:
                    subCat.append(catResp['title']);
            idx = idx+1;

    subCat = list(set(subCat));
    # print subCat;
    for subcat in subCat:
        artParams = {'action':'query', 'list':'categorymembers', 'cmtitle':subcat, 'format':'json'}
        jsonResp = requests.get(WIKI_API, artParams).json();
        if 'query' not in jsonResp or 'categorymembers' not in jsonResp['query']:
            continue;
        for artResp in jsonResp['query']['categorymembers']:
            articleList.append(artResp['title']);
        while('continue' in jsonResp):
            artParams['cmcontinue'] = jsonResp['continue']['cmcontinue'];
            jsonResp = requests.get(WIKI_API, artParams).json();
            if 'query' not in jsonResp or 'categorymembers' not in jsonResp['query']:
                continue;
            for artResp in jsonResp['query']['categorymembers']:
                articleList.append(artResp['title']);
    articleList = list(set(articleList));
    # print articleList;
    return (subCat,articleList);
#t = getArticles(0, "Machine learning");
#print len(t[0])
#print len(t[1])