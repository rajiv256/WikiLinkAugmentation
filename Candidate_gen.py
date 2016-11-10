import  wikipedia as wi
from bs4 import BeautifulSoup as bs

from content import *
from tfidf import *
import ArticleClass
#from google_search import *
from variable import allTfIdf
import pickle

def generate_candidates(article):
    categories = pruneCategories(article)
    print categories
    sub_articles = []
    for catgry in categories:
        sub_articles += getArticles(0 , catgry)
    print sub_articles
    pruned_article =[]
    '''
    for cad_article in sub_articles:
        relevant = similaritycheck(article.title,cad_article.title)
        if(relevant == True):
            pruned_article += [cad_article]
    print pruned_article
    '''


global allTfIdf
allTfIdf = pickle.load(open("AlldocTfIdfs_mini.pkl", "rb" ))
print len(allTfIdf)


allTfIdf = map(lambda p : (p[0] , (p[1],p[2])) , allTfIdf)
allTfIdf = dict(allTfIdf)
wordDs = pickle.load( open("wordDs_mini.pkl", "rb") )
Allwords = pickle.load( open("Allwords_mini.pkl", "rb") )
N = len(allTfIdf.keys())
setallglobals(wordDs,Allwords,N)
print "setted all globals"


print allTfIdf
target_article = ArticleClass.Article("Iterator")
generate_candidates(target_article)