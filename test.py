import  wikipedia as wi
from bs4 import BeautifulSoup as bs
from ArticleClass import *
from variable import allTfIdf
from content import *
from tfidf import *
import pickle

global allTfIdf
allTfIdf = pickle.load(open("AlldocTfIdfs_mini.pkl", "rb" ))
allTfIdf = map(lambda p : (p[0] , (p[1],p[2])) , allTfIdf)
allTfIdf = dict(allTfIdf)
wordDs = pickle.load( open("wordDs_mini.pkl", "rb") )
Allwords = pickle.load( open("Allwords_mini.pkl", "rb") )
N = len(allTfIdf.keys())
setallglobals(wordDs,Allwords,N)
print "setted all globals"
print wordDs
print N
target_article = "Iterator"
target_a = Article("Iterator")
print "article created succesfully"
artlist = giveSimArtcls(target_a,0.10)
print artlist
