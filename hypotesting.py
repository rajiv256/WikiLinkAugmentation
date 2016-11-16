# coding=utf-8
import time
import wikipedia
import pickle
from categories import *
from content import *
from tfidf import *


#To calculate Tfidf and word concept vector
Alldocumentstitles = []
f = open("download_mini","r")
target = open("Alltitles_mini","w")
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
# Alldocumentstitles = Alldocumentstitles[500:1000]
# index = 0.5
Alldocuments = []
Allhtmls = []
start = time.time()
# i = 0
# while i<len(All):
presentdocs = Alldocumentstitles    #[i:i+50]
#     i=i+50
print presentdocs

htmlcontents = filter(lambda y: (y[1] != "NULL"), zip(presentdocs,map(lambda p : giveRawContent(p)  , presentdocs )))

Alldocuments += map(lambda p : (htmlcontents[p][0], htmlcontents[p][1][0] ,htmlcontents[p][1][2] ) , range(len(htmlcontents)))
Allhtmls += map(lambda p : (htmlcontents[p][0], htmlcontents[p][1][1] ) , range(len(htmlcontents)))
pickle.dump(Allhtmls, open("Allhtmls_mini.pkl", "wb"))
# print "filtering doing", i
# print "content obtained", i
pickle.dump(Alldocuments, open("Alldocuments_mini.pkl", "wb"))

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
