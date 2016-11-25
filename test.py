# coding=utf-8
import  wikipedia as wi
from bs4 import BeautifulSoup as bs
import ArticleClass
import variable
import sys
from content import *
from tfidf import *
import pickle
from scoring import *

documents_pickle = "pickles/Alldocuments.pkl"
htmls_pickle = "pickles/Allhtmls.pkl"

Alldocuments = pickle.load(open(documents_pickle, "rb" ))
print (len(Alldocuments))

#Alldocuments = map(lambda p : (p[0] ,givePrunedContent("NULL", p[1]),giveSummary("NULL" , p[2]) )  ,Alldocuments )
Alldocuments = pickle.load(open("pickles/Alldocuments_pruned_content_short.pkl", "rb") )
print "done with loading"


Alldocuments1 = map(lambda p : (p[0] , (p[1] , p[2]) ),Alldocuments )
variable.Allcontent = dict(Alldocuments1)
print (len(Alldocuments))
N = len(Alldocuments)
#clcaulting all preliminary things
#(wordDs,Allwords,N)  = calculateDs(Alldocuments)
print "CalculateDs Done"
#pickle.dump(wordDs, open("pickles/wordDs_short1.pkl", "wb"))
#pickle.dump(Allwords, open("pickles/Allwords_short1.pkl", "wb"))
wordDs = pickle.load(open("pickles/wordDs_short.pkl", "rb"))
Allwords = pickle.load(open("pickles/Allwords_short.pkl", "rb"))
print len(Allwords)
#variable.allTfIdf = map(lambda p : (p[0] , (TfIdf(p[1]) ,TfIdf(p[2]) ) ), Alldocuments)
#variable.allTfIdf = dict(variable.allTfIdf)
variable.allTfIdf = pickle.load(open("pickles/allTfIdf_short.pkl", "rb"))
print "Done with tfidfs"
#pickle.dump(variable.allTfIdf, open("pickles/allTfIdf_short1.pkl", "wb"))
setallglobals(wordDs,Allwords,N,wordConceptMatrix)

#wordConceptMatrix = Invertedindex(variable.allTfIdf.items())
wordConceptMatrix  = pickle.load(open("pickles/WordConceptMatrix_short.pkl", "rb"))
#print map(lambda p : len(p[1].items()) , wordConceptMatrix)

wordConceptMatrix = sortwordconceptmatrix(wordConceptMatrix)
print len(wordConceptMatrix)
wordConceptMatrix = dict(wordConceptMatrix)


print "Done with Concept matrix"
#pickle.dump(wordConceptMatrix, open("pickles/WordConceptMatrix_short1.pkl", "wb"))

setallglobals(wordDs,Allwords,N,wordConceptMatrix)

variable.allhtmls = pickle.load(open(htmls_pickle, "rb" ))
variable.allhtmls  = dict(variable.allhtmls)
#print variable.allhtmls.keys()
print "Done with htmls"
print N
print "setted all globals"

'''
target_a = ArticleClass.Article("Prim's algorithm")
print len(target_a.contentTfIdf)
d = DocConceptVector(target_a.contentTfIdf)
print "Prim's algorithm"
print sorted(d.items() , key = lambda p :p[1],reverse = True )[:100]
'''

'''
target_a = ArticleClass.Article("Prim's algorithm")
relarticles = [ "Dijkstra's algorithm"]

print target_a.summryTfIdf

d = SummarySim(target_a,relarticles)

print d
#print "Dijsktra algorithm"
#print sorted(d.items() , key = lambda p :p[1],reverse = True )[:100]
'''

'''
target_a = ArticleClass.Article("Boundary particle method")
target_a = fill_links(target_a)
print target_a.hyperlinks
'''



start = time.time()

testcases = ["Best-first search"]



'''
testcases = ["Double-ended queue","Stack (abstract data type)","Iterator","Dijkstra's algorithm","Kruskal's algorithm",
                 "Ford–Fulkerson algorithm","Prim's algorithm","CYK algorithm","Priority queue","Bubble sort","Insertion sort",
                 "Smooth sort","Merge sort","Sion's minimax theorem","Minimax","JH (hash function)","Big O notation","Flajolet-Martin algorithm",
                 "Johnson's algorithm","AdaBoost"]
'''

#links = map(lambda p : (p , see_also(p) ) , testcases)
#map( lambda p :see_also_or_not(p[0] , p[1] ) , links)
makesamplecase_relarticleswrite(testcases , "testing/smalltescase1")

makesamplecase_findrelarticles( "testing/small_outputfile1" , "testing/small_suggestions1.txt" ,
                                "testing/smalltescase1" , "testing/Actual_see_also_new1" )

# table  = make_table("Queue (abstract data type)")
# print table
# writeToFile(table)


end =time.time()
print (end-start)

