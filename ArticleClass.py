import variable
import tfidf
from content import givePrunedContent,giveSummary


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
        self.successful = True
        if title not in variable.allTfIdf.keys():
            print ("Title: " + title)
            Content = givePrunedContent(title,"NULL")
            if(Content == "NULL"):
                self.successful = False
            else:
                self.contentTfIdf = tfidf.TfIdf(Content);
                summary = giveSummary(title,"NULL")
                self.summryTfIdf = tfidf.TfIdf(summary);
                self.content = Content
                self.summary = summary
                variable.allTfIdf[title] = (self.contentTfIdf,self.summryTfIdf);
                variable.Allcontent[title] = (self.content,self.summary)
        else:
            self.contentTfIdf = variable.allTfIdf[title][0]
            self.summryTfIdf = variable.allTfIdf[title][1]
            self.content = variable.Allcontent[title][0]
            self.summary = variable.Allcontent[title][1]