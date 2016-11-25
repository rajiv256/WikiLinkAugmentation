
import math
import itertools
from _ast import In
from collections import Counter
import pickle
# from nltk.corpus.reader.util import concat
import time

wordDs ={}
Allwords = []
N = 0
wordConceptMatrix = {}

def setallglobals(w,A,n,wcm):
    global wordDs
    global  Allwords
    global  N
    global wordConceptMatrix
    wordDs = w
    Allwords = A
    N = n
    wordConceptMatrix = wcm
    return


'''
def add(wordfrequencies,p):
    if p in wordfrequencies.keys():
        wordfrequencies[p] += 1
    else:
        wordfrequencies[p] = 1
    return 0

def addword(word,words):
    if(word not in words):
        words += [word]
    return 0

def add(lists , list):
    lists = lists + list
    return 0
'''
def calculateDs(Alldocuments):
    global wordDs
    global Allwords
    global N
    Allwords = []
    N = len(Alldocuments)
    docwords = map(lambda p : p[1].split(" ") ,Alldocuments)
    Allwords = sum(docwords , [])
    Allwords = list(set(Allwords))
    #wordcounts = map( lambda doc : map( lambda p : (1 if (Allwords[p] in doc[1]) else 0 )  , range(len(Allwords)) ),Alldocuments )
    length = len(Allwords)
    print length
    i = 0
    wordds = []
    while (i < length):
        wordds += map(lambda p : (Allwords[p] , sum(map(lambda doc : (1 if (Allwords[p] in doc[1]) else 0) ,Alldocuments ))), range(i,min(i+1000,length)) )
        i = i + 1000
        print i

    wordDs = dict(wordds)
    return (wordDs,Allwords ,N)

def linkTfIdf(links):
    termfrequencies = dict(Counter(links))
    docwords = termfrequencies.keys();
    InverseDocfreq = map(lambda p: (p, math.log(N / min(map(lambda p : wordDs[p] if p in Allwords else 1 ,docwords) + [1]) )), docwords)
    tfidf = map(lambda p: (p[0], termfrequencies[p[0]] * p[1]), InverseDocfreq)
    tfidf = dict(tfidf)
    return tfidf

def Tf(document):
    docwords = document.split(" ")
    termfrequencies = dict(Counter(docwords));
    return termfrequencies


Completedtfidf = 0
def TfIdf(document):
    global Completedtfidf
    global Allwords
    docwords = document.split(" ")
    termfrequencies = dict(Counter(docwords));
    docwords = termfrequencies.keys();
    localwordDs = {}
    Completedtfidf += 1
    print Completedtfidf
    for x in docwords:
        if (x in Allwords):
            Allwords += [x]
            localwordDs[x] = wordDs[x]
        else:
            localwordDs[x] = 1
    InverseDocfreq = map(lambda p : (p , math.log( N / localwordDs[p] ) ) ,docwords)
    tfidf = map (lambda p : (p[0],termfrequencies[p[0]]*p[1]) ,InverseDocfreq )
    tfidf = dict(tfidf)
    return tfidf


def Invertedindex(Alldocuments):
    global wordConceptMatrix
    AllTfIdfs = map(lambda  doc :   (doc[0] , doc[1][0] )  ,Alldocuments)
    if 'treehowever' in Allwords:
        print 'yes'
    length = len(Allwords)
    print length
    wordConceptMatrixlist = []
    wordConceptMatrixlist = pickle.load(open("pickles/WordConceptMatrix_short.pkl", "rb"))
    print len(wordConceptMatrixlist)
    print wordConceptMatrixlist[0]
    size = len(wordConceptMatrixlist)
    i = size
    print length
    while(i < length):
        wordConceptMatrixlist += map(lambda p : (Allwords[p],makeWordconceptvector(AllTfIdfs,Allwords[p])) , range(i,min(i+1000,length)) )
        i += 1000;
        print i
        if( (i)% 5000 == 0):
            print "dumping"
            pickle.dump(wordConceptMatrixlist, open("pickles/WordConceptMatrix_short.pkl", "wb"))
    wordConceptMatrixtest = map(lambda p : p[0] , wordConceptMatrixlist)
    pickle.dump(wordConceptMatrixlist, open("pickles/WordConceptMatrix_short.pkl", "wb"))
    print len(wordConceptMatrixlist)
    wordConceptMatrix = wordConceptMatrixlist
    return wordConceptMatrix

def makeWordconceptvector(tfidfs ,word):
    conceptvector={}
    threshold = 0.1;
    for t in tfidfs:
        contenttfidf = t[1]
        if word in contenttfidf.keys():
            if(contenttfidf[word] > threshold):
                conceptvector[t[0]] = contenttfidf[word]
    return conceptvector



def dotproduct(conceptrelev,wordrelev):
    return sum(map (lambda p: conceptrelev[p]*wordrelev[p] ,range(len(wordrelev)) ))
def DocConceptVector(Doctfidf):
    doctfidf = Doctfidf
    #doctfidf = TfIdf(document)
    taken = int(math.ceil(len(doctfidf)*0.6 ))
    doctfidf = dict ( sorted(doctfidf.items() , key = lambda p : p[1] ,reverse = True)[:taken] )
    doctfidfkeys = list(filter(lambda p: p in Allwords , doctfidf.keys() ) )
    #doctfidfkeys = list(filter(lambda p: wordConceptMatrix[p] != {}, doctfidfkeys ))
    localwordConceptMatrix = dict ( map(lambda p : (p , wordConceptMatrix[p] ), doctfidfkeys ) )
    allocalConcepts = map(lambda p : localwordConceptMatrix[p].keys() ,doctfidfkeys)
    print len(allocalConcepts[1])
    allocalConcepts = list(itertools.chain(*allocalConcepts))
    allocalConcepts = list(set(allocalConcepts))
    print len(allocalConcepts)
    print "2"
    start = time.time()
    localwordConceptMat = map(lambda p:(map(lambda concept : localwordConceptMatrix[p][concept] if concept in localwordConceptMatrix[p] else 0,allocalConcepts) ), doctfidfkeys )
    print "3"
    end = time.time()
    print (end-start)
    localwordConceptMatT = map(list,zip(*localwordConceptMat))
    doctfidfvalues = map(lambda p : doctfidf[p],doctfidfkeys )
    conceptvector =  map(lambda p : dotproduct( p,doctfidfvalues) , localwordConceptMatT)
    print "4"
    conceptvector = zip(allocalConcepts ,conceptvector)
    return dict(conceptvector)

def CosSim(tfidf1,tfidf2):
    len1 = len(tfidf1)
    mag1 = math.sqrt(sum(map(lambda p : p[1]*p[1],tfidf1.items())))
    mag2 = math.sqrt(sum(map(lambda p : p[1]*p[1],tfidf2.items())))
    words1  = tfidf1.keys()
    words2 = tfidf2.keys()
    sim =0
    for i in words1:
        if i in words2:
            sim += tfidf2[i]*tfidf1[i]
    if(mag1 ==0 or mag2==0 ):
        return 0
    sim = float(sim) / (mag1*mag2)
    return sim;
def ConceptVectorSimilarity(TfIdf1,TfIdf2):
    print "getting Doc vector similarity"
    start = time.time()
    print len(TfIdf1)
    print len(TfIdf2)
    conceptvector1 = DocConceptVector(TfIdf1)
    conceptvector2 = DocConceptVector(TfIdf2)
    print "Done getting Doc vector similarity "
    end = time.time()
    print (end-start)
    similarity = CosSim(conceptvector1,conceptvector2)
    return similarity

#taking only top 100 concepts for all words
def sortwordconceptmatrix(wordconpmatrix):
    wordconpmatrix = map(lambda  p : ( p[0] , dict(sorted( p[1].items() ,key =lambda x : x[1] , reverse = True)[:100])  )   , wordconpmatrix)
    return wordconpmatrix