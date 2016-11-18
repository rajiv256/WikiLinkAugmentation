from parser import *
from ArticleClass import *


query = 'New York'

print len(summary_links(query))
print " "

f = open('download_categories','r')
all_categories = []
while (True) :
    s = f.readline()
    if (len(s)==0) :
        break
    splits = s.split(",")
    ss =  splits[1]
    name = ss.split(":")[1][:-1]
    name = str(name)
    name = name.replace("_"," ")
    all_categories.append(name)
f.close()
