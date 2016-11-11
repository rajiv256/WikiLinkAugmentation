import  wikipedia as wi
from bs4 import BeautifulSoup as bs

import ArticleClass
import variable
from content import *
from tfidf import *

import pickle


variable.allTfIdf = pickle.load(open("AlldocTfIdfs_mini.pkl", "rb" ))
variable.allTfIdf = map(lambda p : (p[0] , (p[1],p[2])) , variable.allTfIdf)
variable.allTfIdf = dict(variable.allTfIdf)
wordDs = pickle.load( open("wordDs_mini.pkl", "rb") )
Allwords = pickle.load( open("Allwords_mini.pkl", "rb") )
N = len(variable.allTfIdf.keys())
wordConceptMatrix = Invertedindex(variable.allTfIdf.items())

setallglobals(wordDs,Allwords,N,wordConceptMatrix)
print N
print "setted all globals"



#print wordDs

#print Allwords



'''
contenthtml = givePrunedContent(title)
print 'newtfidf'
tfs = Tf(contenthtml[0])
tfidf = TfIdf(contenthtml[0])
ds = {}
for word in tfs.keys():
    if( word in wordDs):
        ds[word] = (wordDs[word],tfs[word],tfidf[word])
ds = map(lambda p : (p[0],p[1][0],p[1][1],p[1][2]) ,ds.items())
ds = sorted(ds , key = lambda p : p[3])
#print ds
#print TfIdf(contenthtml[0])
'''

'''
target_article = "Iterator"
target_a = ArticleClass.Article("Iterator")
print "article created succesfully"
artlist = pruneCategories(target_a)
print artlist
'''
'''
test =  variable.allTfIdf['Fibonacci heap']
test = test[0].items()

sortedtfidf = sorted( test,key = lambda p : p[1] ,reverse = True)
print sortedtfidf
sortedtfidf = sortedtfidf[:10]
for key in sortedtfidf:
    print (key ,  wordConceptMatrix[key[0]])
'''


'''
sim = ConceptVectorSimilarity(variable.allTfIdf['Fibonacci heap'][0] ,variable.allTfIdf['Iterator'][0] )
print sim
'''

