from variable import *;
from tfidf import *
from content import *

class Article:
    '''Article Class'''

    def __init__(self, title):
        self.title = title;
        self.content  = ""
        self.summary = ""
        self.contentTfIdf = {}
        self.summryTfIdf = {}
        self.summaryhyperlinks =[] #(word :link)
        self.hyperlinks = []
        self.SeeAlso = []
        self.Categories = []
        self.PrunedCategories = []
        if title not in allTfIdf.keys():
            self.contentTfIdf = TfIdf(givePrunedContent(title));
            self.summryTfIdf = TfIdf(giveSummary(title));
            allTfIdf[title] = (self.contentTfIdf,self.summryTfIdf);
        else:
            self.contentTfIdf = allTfIdf[title][0]
            self.summryTfIdf = allTfIdf[title][1]
