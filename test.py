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
print "CalculateDs DOne "
#pickle.dump(wordDs, open("pickles/wordDs_short.pkl", "wb"))
#pickle.dump(Allwords, open("pickles/Allwords_short.pkl", "wb"))
wordDs = pickle.load(open("pickles/wordDs_short.pkl", "rb"))
Allwords = pickle.load(open("pickles/Allwords_short.pkl", "rb"))
print len(Allwords)
#variable.allTfIdf = map(lambda p : (p[0] , (TfIdf(p[1]) ,TfIdf(p[2]) ) ), Alldocuments)
#variable.allTfIdf = dict(variable.allTfIdf)
variable.allTfIdf = pickle.load(open("pickles/allTfIdf_short.pkl", "rb"))
print "Done with tfidfs"
#pickle.dump(variable.allTfIdf, open("pickles/allTfIdf_short.pkl", "wb"))
print len(Allwords)
Allwordstest = list(set(Allwords))
print len(Allwordstest)
setallglobals(wordDs,Allwords,N,wordConceptMatrix)

#wordConceptMatrix = Invertedindex(variable.allTfIdf.items())
wordConceptMatrix  = pickle.load(open("pickles/WordConceptMatrix_short.pkl", "rb"))
#print map(lambda p : len(p[1].items()) , wordConceptMatrix)

wordConceptMatrix = sortwordconceptmatrix(wordConceptMatrix)
#print len(wordConceptMatrix[100][1].items())
wordConceptMatrix = dict(wordConceptMatrix)


print "Done with Concept matrix"
#pickle.dump(wordConceptMatrix, open("pickles/WordConceptMatrix_short.pkl", "wb"))

setallglobals(wordDs,Allwords,N,wordConceptMatrix)

variable.allhtmls = pickle.load(open(htmls_pickle, "rb" ))
variable.allhtmls  = dict(variable.allhtmls)
#print variable.allhtmls.keys()
print "Done with htmls"
print N
print "setted all globals"


target_a = ArticleClass.Article("Prim's algorithm")
print len(target_a.contentTfIdf)
d = DocConceptVector(target_a.contentTfIdf)
print "Prim's algorithm"
print sorted(d.items() , key = lambda p :p[1],reverse = True )[:100]

'''
target_a = ArticleClass.Article("Dijkstra's algorithm")
print len(target_a.contentTfIdf)
d = DocConceptVector(target_a.contentTfIdf)
print "Dijsktra algorithm"
print sorted(d.items() , key = lambda p :p[1],reverse = True )[:100]
'''

'''
target_a = ArticleClass.Article("Boundary particle method")
target_a = fill_links(target_a)
print target_a.hyperlinks
'''

'''
target_a = ArticleClass.Article("All-serial CORDIC")
relarticles = allrelevantarticles(target_a)
relarticles = map(lambda p: p.split("Category:")[1] if ("Category" in p) else p, relarticles)
print "all relevant articles"
print relarticles
start = time.time()
#s = hyperlinksimilarity(target_a,target_b)
hyperlink_similarities = hyperlinkSim(target_a, relarticles)

end = time.time()
print (end-start)
hyperlink_similarities = map(lambda p: (p[0].title, p[1]), hyperlink_similarities)
hyperlink_similarities = dict(hyperlink_similarities)
print 'hyperlink-similarity done'
'''

#print (variable.allhtmls["Ford–Fulkerson algorithm"])
s = "Ford–Fulkerson algorithm"
s.decode('utf-8').encode('ascii','replace').replace("?"," ")
print s
'''
start = time.time()
makesamplecase( ["Double-ended queue","Stack (abstract data type)","Iterator","Dijkstra's algorithm","Kruskal's algorithm",
                 "Ford–Fulkerson algorithm","Prim's algorithm","CYK algorithm","Priority queue","Bubble sort","Insertion sort",
                 "Smooth sort","Merge sort","Sion's minimax theorem","Minimax","JH (hash function)","Big O notation","Flajolet-Martin algorithm",
                 "Johnson's algorithm","AdaBoost"] , "outputfile3" , "suggestions3.txt" , "SampleArticles")
# table  = make_table("Queue (abstract data type)")
# print table
# writeToFile(table)
end =time.time()
print (end-start)
'''
