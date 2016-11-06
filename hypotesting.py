# coding=utf-8
import time
import wikipedia
import pickle
from categories import *
from content import *
from tfidf import *


#To calculate Tfidf and word concept vector
Alldocumentstitles = []
f = open("download_short","r")
target = open("Alltitles_short","w")
line = f.readline()
line = f.readline()
while(line):
    line = line.split(",")
    line = line[1][1:]
    line = line[:len(line)-1].replace('_',' ')
    Alldocumentstitles += [line]
    target.write(line + "\n")
    line = f.readline()

target.flush()
target.close()

print len(Alldocumentstitles)

#check
#Alldocumentstitles = Alldocumentstitles[:]

start = time.time()
Alldocuments = map(lambda p : (p, givePrunedContent(p),giveSummary(p) ) , Alldocumentstitles)
print "content obtained"
Alldocuments = list(filter(lambda p : (p[1]!="NULL" and p[2]!="NULL") , Alldocuments ))
print "filtering doing"
#pickle.dump(Alldocuments, open( "Alldocuments.pkl", "wb" ) )


(wordDs,Allwords,N) = calculateDs(Alldocuments)
print len(wordDs.keys())
print wordDs
print len(Allwords)
print Allwords
print N
pickle.dump(wordDs, open("wordDs_short.pkl", "wb") )
pickle.dump(Allwords, open("Allwords_short.pkl", "wb") )
print "wordDs obtained"

AllTfIdfs = map(lambda doc: (doc[0], TfIdf(doc[1]) ,TfIdf(doc[2]) ), Alldocuments)
pickle.dump(Allwords, open("AlldocTfIdfs_short.pkl", "wb") )
end =time.time()
print (end-start)
#pickle.dump(N, open( "N.pkl", "wb" ) )
#wordConceptVector = Invertedindex(Alldocuments)
#print wordConceptVector






