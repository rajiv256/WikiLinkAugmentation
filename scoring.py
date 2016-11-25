#The One with all the scoring
#he he he
import ArticleClass
import variable
from content import *
from tfidf import *
import random
from google_search import *


def make_table(title):
    target_a = ArticleClass.Article(title)
    print "article created succesfully"
    #artlist = giveSimArtcls(target_a,0)
    relarticles = allrelevantarticles(target_a)
    if title in relarticles:
        relarticles.remove(title)
    relarticles = map(lambda p : p.split("Category:")[1] if ("Category:" in p) else p , relarticles )
    print "all relevant articles"
    print relarticles
    relarticles = prune_articles(target_a,relarticles)
    return relarticles

    '''
    simDict = referenceSimilarity(target_a.title,relarticles)
    print simDict
    print "reference similarity done"
    content_based_sim = contentSim(target_a,relarticles)
    content_based_sim = map(lambda p : (p[0].title ,p[1]) ,content_based_sim )
    content_based_sim = dict(content_based_sim)
    print 'content-based-similarity done'
    hyperlink_similarities = hyperlinkSim(target_a,relarticles)
    hyperlink_similarities = map(lambda p : (p[0].title ,p[1]) ,hyperlink_similarities )
    hyperlink_similarities = dict(hyperlink_similarities)
    print 'hyperlink-similarity done'
    #articles_for_google = map(lambda p : p[0] , content_based_sim.items() )[10 : ]
    #google_similarities = getCandidateSimilarity(target_a.title,articles_for_google,2)
    #print "google - similarity"
    # google_similarities[p] if (p in google_similarities.keys()) else  0
    table = map(lambda p : (title, p ,  simDict[p], content_based_sim[p][1] ,hyperlink_similarities[p]  , see_also_or_not(title,p) ) , relarticles )
    table = sorted(table,key = lambda p : p[5] , reverse = True)
    print "normal table done"
    table = final_scores(table)

    table = []
    return table
    '''

def writeToFile(table,filename):
    target = open(filename , 'w')
    target.truncate()
    for t in table:
        for i in range(len(t)):
            target.write(str(t[i]) + " ")
        target.write("\n")
    target.flush()
    target.close()

def writeToFile2(s , table,filename ):
    target = open(filename, 'a')
    target.truncate()
    for t in table:
        target.write(s + "$"  + t)
        target.write("\n")
    target.flush()
    target.close()


def gettestcases(filename):
    f = open(filename, 'r')
    line =f.readline()
    testcases = {}
    while(line):
        line = line.split("$")
        if(line[0] not in testcases.keys()):
            testcases[line[0]] = []
        testcases[line[0]] += [line[1]]
    return testcases

def makesamplecase(filename1 ,suggfile):
    allarticles = variable.allTfIdf.keys();
    #taking 20 samples
    sample = random.sample( allarticles , 1000 )
    print "getting titles with see_also"
    only_see_also_articles = filter(lambda p: len(see_also(p)) > 0,  sample)
    print "done"
    sample = random.sample(only_see_also_articles, 30)
    print sample
    Table = []
    Ranking = []
    for s in sample:
        table = make_table( s )
        writeToFile2(s, table, "SampleArticles")
        #Ranking += combined_score(table)
        Table += table
        #writeToFile(Ranking, suggfile)
        #writeToFile(Table, filename1)

    #writeToFile(Ranking, suggfile)
    #writeToFile(Table,filename1)

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


def combined_score(table):
    combinedscore = map(lambda p :  (p[1], sum(p[2]) ,p[3] ) , table)
    return sorted(combinedscore , key = lambda p : p[1],reverse = True)



def prune_articles(target_a,relarticles):
    relarticles = SummarySim(target_a,relarticles)
    articles_stored = variable.allTfIdf.keys()
    see_also_articles = see_also(target_a.title)
    see_also_articles = filter(lambda p: (p in articles_stored), see_also_articles)
    relarticles = relarticles[:20] + see_also_articles
    relarticles = list(set(relarticles))

    print "pruned_articles"
    relarticles = map(lambda p: (p[0].title, p[1]), relarticles)
    print relarticles
    return map(lambda p : p[0] , relarticles)

