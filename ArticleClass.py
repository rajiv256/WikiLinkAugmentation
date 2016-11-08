from variable import *;
from tfidf import *
from content import *
class Article(object):
    '''Article Class'''
    title = ""
    content  = ""
    summary = ""
    contentTfIdf = {}
    summryTfIdf = {}
    summaryhyperlinks =[] #(word :link)
    hyperlinks = []
    SeeAlso = []
    Categories = []
    PrunedCategories = []

    def __init__(self, title):
        self.title = title;
        if title not in allTfIdf.keys():
            self.contentTfIdf = TfIdf(givePrunedContent(title));
            self.summryTfIdf = TfIdf(giveSummary(title));
            allTfIdf[title] = (self.contentTfIdf,self.summryTfIdf);
        else:
            self.contentTfIdf = allTfIdf[title][0]
            self.summryTfIdf = allTfIdf[title][1]
