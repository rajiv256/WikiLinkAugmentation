#The One with all the scoring
#he he he
import ArticleClass
import variable
from content import *
from tfidf import *
import random

def make_table(title):
    target_a = ArticleClass.Article(title)
    print "article created succesfully"
    #artlist = giveSimArtcls(target_a,0)
    relarticles = allrelevantarticles(target_a)
    relarticles = map(lambda p : p.split("Category:")[1] if ("Category" in p) else p , relarticles )
    print "all relevant articles"
    print relarticles

    simDict = referenceSimilarity(target_a.title,relarticles)
    print simDict

    content_based_sim = contentSim(target_a,relarticles)

    content_based_sim = map(lambda p : (p[0].title ,p[1]) ,content_based_sim )
    content_based_sim = dict(content_based_sim)
    print 'content-based-similarity done'
    hyperlink_similarities = hyperlinkSim(target_a,relarticles)
    hyperlink_similarities = map(lambda p : (p[0].title ,p[1]) ,hyperlink_similarities )
    hyperlink_similarities = dict(hyperlink_similarities)
    print 'hyperlink-similarity done'
    table = map(lambda p : (title, p , simDict[p], content_based_sim[p][1] ,hyperlink_similarities[p] , see_also_or_not(title,p) ) , relarticles )
    table = sorted(table,key = lambda p : p[5] , reverse = True)
    print "normal table done"
    table = final_scores(table)
    return table


def writeToFile(table,filename):
    target = open(filename , 'w')
    target.truncate()
    for t in table:
        for i in range(len(t)):
            target.write(str(t[i]) + " ")
        target.write("\n")
    target.flush()
    target.close()

def makesamplecase():
    allarticles = variable.allTfIdf.keys();
    #taking 20 samples
    sample = random.sample( range(len(allarticles)) , 2 )
    print map(lambda p : allarticles[p] ,sample)
    Table = []
    Ranking = []
    for s in sample:
        table = make_table(allarticles[s])
        Ranking += combined_score(table)
        Table += table
        writeToFile(Ranking, 'suggestions.txt')
        writeToFile(Table, 'output2.txt')
    writeToFile(Ranking, 'suggestions.txt')
    writeToFile(Table,'output2.txt')

tuple_size = 6    # Size of the scores tuple with candidate
import numpy


def mean_std(l) :
    mean = float(sum(l))/len(l)
    std = numpy.std(l)
    return (mean,std)

def normalize(table) :
    sz = len(table[0])
    for j in range(sz) :
        l = []
        for k in table :
            l.append(k[j])
        meanstd = mean_std(l)
        minx = min(l)
        maxx = max(l)
        for i in range(len(l)) :
            l[i] = float(l[i]-minx)/(maxx-minx+0.00000001)
        for i in range(len(table)) :
            table[i][j] = l[i]
    return table

#print normalize([[1,1,1,1],[2,2,2,2]])
def split_tuple(tuple) :
    candidates = []
    sz = len(tuple[0])
    x = [0 for i in range(sz-1)]
    table = []
    for i in range(len(tuple)) :
        table.append([])
        for j in range(sz-1) :
            table[-1].append(0)
    for i in range(len(tuple)) :
        candidates.append(tuple[i][0])
    for i in range(len(tuple)) :
        #print table
        for j in range(1,sz) :
            table[i][j-1] = tuple[i][j]
    return (candidates,table)

#returns a tuple
#first element will be a list of candidates
#next element will be a table...each row contains scores of the corresponding candidate in the candidates list.

def final_scores(tuples) :
    target = tuples[0][0]
    label = []
    for i in range(len(tuples)) :
        label += [tuples[i][len(tuples[i]) - 1]]
        tuples[i] = tuples[i][1: (len(tuples[i]) -1 ) ]
    ret = split_tuple(tuples)
    candidates = ret[0]
    scores = normalize(ret[1])
    return map(lambda p : (target, candidates[p] , scores[p] ,label[p] ) , range(len(scores)) ) ;
#print final_scores([("hell","hath",1,1,1,1,1,1),("hell","fury",2,2,2,2,2,2)])


def combined_score(table):
    combinedscore = map(lambda p :  (p[1], sum(p[2]) ,p[3] ) , table)
    return sorted(combinedscore , key = lambda p : p[1])
