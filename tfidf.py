
import math
from _ast import In

wordDs ={}
Allwords = []
N = 0
wordConceptVector = {}

def setN(x,y):
    global N
    global ds
    N = x
    ds = y

def printN():
    print N
    print ds



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

def calculateDs(Alldocuments):
    global wordDs
    global Allwords
    global N
    Allwords = []
    N = len(Alldocuments)
    for doc in Alldocuments:
        docwords = doc[1].split(" ")
        map(lambda p : addword(p , Allwords) ,docwords )
    print Allwords
    wordcounts = map( lambda doc : map( lambda p : (1 if (Allwords[p] in doc[1]) else 0 )  , range(len(Allwords)) ),Alldocuments )
    wordDs = map(  lambda p : (Allwords[p] , sum([wordcounts[i][p] for i in range(len(wordcounts)) ]) ) , range(len(Allwords)) )
    wordDs = dict(wordDs)
    return (wordDs,Allwords ,N)

def linkTfIdf(links):
    termfrequencies = {}
    map(lambda p: add(termfrequencies, p), links);
    docwords = termfrequencies.keys();
    InverseDocfreq = map(lambda p: (p, math.log(N / min(map(lambda p : wordDs[p] if p in Allwords else 0 ,docwords) + [1]) )), docwords)
    tfidf = map(lambda p: (p[0], termfrequencies[p[0]] * p[1]), InverseDocfreq)
    tfidf = dict(tfidf)
    return tfidf


def TfIdf(document):
    docwords = []
    if(isinstance(document , basestring)):
        docwords = document[0].split(" ")
    else:
        docwords = document
    termfrequencies = {}
    map(lambda p : add(termfrequencies,p)  ,docwords);
    docwords = termfrequencies.keys();
    localwordDs = {}
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
    AllTfIdfs = map(lambda  doc :   (doc[0] , TfIdf(doc))  ,Alldocuments)
    wordConceptMatrix1ist = map(lambda p : (p,makeWordconceptvector(AllTfIdfs,p)) , Allwords)
    wordConceptMatrix = dict(wordConceptMatrix1ist)
    return wordConceptMatrix

def makeWordconceptvector(tfidfs ,word):
    conceptvector={}
    threshold = 0.1;
    for t in tfidfs:
        if word in t[1].keys():
            if(t[1][word] > threshold):
                conceptvector[t[0]] = t[1][word]
    return conceptvector



def dotproduct(conceptrelev,wordrelev):
    return sum(map (lambda p: conceptrelev[p]*wordrelev[p] ,range(len(wordrelev)) ))
def DocConceptVector(document):
    doctfidf = TfIdf(document)
    localwordConceptMat = map(lambda p : wordConceptMatrix[p] ,doctfidf.keys())
    localwordConceptMatT = map(list,zip(*localwordConceptMat))
    doctfidfvalues = doctfidf.values();
    conceptvector =  map(lambda p : dotproduct( p,doctfidfvalues) , localwordConceptMatT)
    return conceptvector

def CosSim(tfidf1,tfidf2):
    len1 = len(tfidf1)
    mag1 = math.sqrt(sum(map(lambda p : (tfidf1[1]*tfidf1[1]) ),tfidf1))
    mag2 = math.sqrt(sum(map(lambda p : (tfidf1[2]*tfidf1[2]) ),tfidf2))
    words1  = tfidf1.keys()
    words2 = tfidf2.keys()
    sim =0
    for i in words1:
        if i in words2:
            sim += tfidf2[i]*tfidf1[1]
    sim = float(sim) / (mag1*mag2)



