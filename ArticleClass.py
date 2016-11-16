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
        self.successful = True
        if title not in variable.allTfIdf.keys():
            Content = content.givePrunedContent(title,"NULL")
            if(Content == "NULL"):
                self.successful = False
            else:
                print "getting content"
                self.contentTfIdf = tfidf.TfIdf(Content);
                self.summryTfIdf = tfidf.TfIdf(content.giveSummary(title,"NULL"));
                variable.allTfIdf[title] = (self.contentTfIdf,self.summryTfIdf);
        else:
            print "Already present"
            self.contentTfIdf = variable.allTfIdf[title][0]
            self.summryTfIdf = variable.allTfIdf[title][1]
