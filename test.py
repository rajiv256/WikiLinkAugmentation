import  wikipedia as wi
from bs4 import BeautifulSoup as bs

import ArticleClass
import variable
from content import *
from tfidf import *

import pickle

Alldocuments = pickle.load(open("Alldocuments_mini.pkl", "rb" ))
Alldocuments = map(lambda p : (p[0] ,givePrunedContent("NULL", p[1]),giveSummary("NULL" , p[2]) )  ,Alldocuments )

#clcaulting all preliminary things
(wordDs,Allwords,N)  = calculateDs(Alldocuments)

variable.allTfIdf = map(lambda p : (p[0] , (TfIdf(p[1]) ,TfIdf(p[2]) ) ), Alldocuments)
variable.allTfIdf = dict(variable.allTfIdf)

setallglobals(wordDs,Allwords,N,wordConceptMatrix)

wordConceptMatrix = Invertedindex(variable.allTfIdf.items())

setallglobals(wordDs,Allwords,N,wordConceptMatrix)
'''
variable.allTfIdf = pickle.load( open("AlldocTfIdfs_mini.pkl", "rb") )
wordDs = pickle.load( open("wordDs_mini.pkl", "rb") )
Allwords = pickle.load( open("Allwords_mini.pkl", "rb") )
N = len(variable.allTfIdf.keys())
'''

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


target_article = "Fibonacci heap"
target_a = ArticleClass.Article("Iterator")
print "article created succesfully"
artlist = giveSimArtcls(target_a,0)


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

