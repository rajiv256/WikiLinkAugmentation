import variable
import tfidf
import content

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
        if title not in variable.allTfIdf.keys():
            print variable.allTfIdf
            self.contentTfIdf = tfidf.TfIdf(content.givePrunedContent(title)[0]);
            self.summryTfIdf = tfidf.TfIdf(content.giveSummary(title));
            variable.allTfIdf[title] = (self.contentTfIdf,self.summryTfIdf);
        else:
            print "Already present"
            self.contentTfIdf = variable.allTfIdf[title][0]
            self.summryTfIdf = variable.allTfIdf[title][1]
