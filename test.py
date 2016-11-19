import  wikipedia as wi
from bs4 import BeautifulSoup as bs

import ArticleClass
import variable
import sys
from content import *
from tfidf import *
import pickle


documents_pickle = "pickles/Alldocuments.pkl"
htmls_pickle = "pickles/Allhtmls.pkl"

Alldocuments = pickle.load(open(documents_pickle, "rb" ))
print (len(Alldocuments))

Alldocuments = map(lambda p : (p[0] ,givePrunedContent("NULL", p[1]),giveSummary("NULL" , p[2]) )  ,Alldocuments )

print "done with loading"
Alldocuments1 = map(lambda p : (p[0] , (p[1] , p[2]) ),Alldocuments )
variable.Allcontent = dict(Alldocuments1)
print (len(Alldocuments))
#clcaulting all preliminary things
(wordDs,Allwords,N)  = calculateDs(Alldocuments)
print "CalculateDs DOne "
pickle.dump(wordDs, open("pickles/wordDs_short.pkl", "wb"))
pickle.dump(Allwords, open("pickles/Allwords_short.pkl", "wb"))

print len(Allwords)
variable.allTfIdf = map(lambda p : (p[0] , (TfIdf(p[1]) ,TfIdf(p[2]) ) ), Alldocuments)
variable.allTfIdf = dict(variable.allTfIdf)

print "Done with tfidfs"

pickle.dump(variable.allTfIdf, open("pickles/allTfIdf_short.pkl", "wb"))


setallglobals(wordDs,Allwords,N,wordConceptMatrix)

wordConceptMatrix = Invertedindex(variable.allTfIdf.items())

print "Done with Concept matrix"
pickle.dump(wordConceptMatrix, open("pickles/WordConceptMatrix_short.pkl", "wb"))


setallglobals(wordDs,Allwords,N,wordConceptMatrix)

variable.allhtmls = pickle.load(open(htmls_pickle, "rb" ))
map(lambda p : (p[0] ,p[1]) , variable.allhtmls )
variable.allhtmls  = dict(variable.allhtmls)
print variable.allhtmls.keys()

print "Done with htmls"
'''
variable.allTfIdf = pickle.load( open("AlldocTfIdfs_mini.pkl", "rb") )
wordDs = pickle.load( open("wordDs_mini.pkl", "rb") )
Allwords = pickle.load( open("Allwords_mini.pkl", "rb") )
N = len(variable.allTfIdf.keys())
'''

print N
print "setted all globals"


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
target_a = ArticleClass.Article("Queue (abstract data type)")
print "article created succesfully"
#artlist = giveSimArtcls(target_a,0)
relarticles = allrelevantarticles(target_a)
print "all relevant articles"
print relarticles

print "reference present links"
simDict = referenceSimilarity(target_a.title,relarticles)
print "Reference similarity"
print simDict
content_based_sim = contentSim(target_a,relarticles)
print "content-based similarity"
justnames = map(lambda p : (p[0].title ,p[1]) ,content_based_sim )
print justnames

hyperlink_similarities = hyperlinkSim(target_a,relarticles[:2])
justnames = map(lambda p : (p[0].title ,p[1]) ,hyperlink_similarities )
print justnames
'''










'''
sim = ConceptVectorSimilarity(variable.allTfIdf['Fibonacci heap'][0] ,variable.allTfIdf['Iterator'][0] )
print sim
'''

