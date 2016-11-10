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
Alldocumentstitles = Alldocumentstitles[:1000]
Alldocuments = []
Allhtmls = []
start = time.time()
i = 0
while i<1000:
    presentdocs = Alldocumentstitles[i:i+50]
    i=i+50
    print presentdocs

    htmlcontents = map(lambda p : givePrunedContent(p)  , presentdocs )
    Alldocuments += map(lambda p : (presentdocs[p], htmlcontents[p][0] ,giveSummary(presentdocs[p]) ) , range(len(presentdocs)))
    Allhtmls += map(lambda p : (presentdocs[p], htmlcontents[p][1] ) , range(len(presentdocs)))
    Allhtmls = list(filter(lambda p: (p[1] != "NULL"), Allhtmls))
    pickle.dump(Allhtmls, open("Allhtmls_short1.pkl", "wb"))
    print "content obtained"
    Alldocuments = list(filter(lambda p : (p[1]!="NULL" and p[2]!="NULL") , Alldocuments ))
    print "filtering doing"
    pickle.dump(Alldocuments, open("Alldocuments_short1.pkl", "wb"))
    #(wordDs,Allwords,N) = calculateDs(Alldocuments)
    #print len(Allwords)
    #print wordDs
    #print Allwords
    #pickle.dump(wordDs, open("wordDs_short1.pkl", "wb") )
    #pickle.dump(Allwords, open("Allwords_short1.pkl", "wb") )
    #print "wordDs obtained"
    #AllTfIdfs = map(lambda doc: (doc[0], Tf(doc[1]) ,Tf(doc[2]) ), Alldocuments)
    #allsums = sum(map(lambda p: sum(p[1].values()) , AllTfIdfs))
    #AllTfIdfs = map(lambda doc: (doc[0], TfIdf(doc[1]) ,TfIdf(doc[2]) ), Alldocuments)
    #pickle.dump(AllTfIdfs, open("AlldocTfs_short1.pkl", "wb") )

end =time.time()
print (end-start)

#wordConceptVector = Invertedindex(Alldocuments)
#print wordConceptVector






