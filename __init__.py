from parser import *
from ArticleClass import *
from xgoogle.search import *

query = 'New York'

print len(summary_links(query))
print " "

#print len(all_links(query))
