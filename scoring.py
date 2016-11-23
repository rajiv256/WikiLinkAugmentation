#The One with all the scoring

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
        print table
        for j in range(1,sz) :
            table[i][j-1] = tuple[i][j]
    return (candidates,table)

#returns a tuple
#first element will be a list of candidates
#next element will be a table...each row contains scores of the corresponding candidate in the candidates list.
def final_scores(tuple) :
    ret = split_tuple(tuple)
    candidates = ret[0]
    scores = normalize(ret[1])
    return (candidates,scores)

