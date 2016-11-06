'''
Article : (content ,summary , hyperlinks, see also, Categories)

'''
from ArticleClass import *
from tfidf import *
from parser import *

def articleSimilarity(article1,article2):
    #Tfidf1 = TfIdf(article1.summary)
    #Tfidf2 = TfIdf(article2.summary)

    Sim1 = CosSim(article1.summryTfidf,article2.summryTfidf)
    if(article1.summaryhyperlinks == []):
        article1 = fill_links(article1.title)
    if(article2.summaryhyperlinks == []):
        article2 = fill_links(article2.title)
    links1 = map(lambda p : p[0] ,article1.summaryhyperlinks())
    links2 = map(lambda p: p[0], article2.summaryhyperlinks())
    linkidf1 = linkTfIdf(links1)
    linkidf2 = linkTfIdf(links2)
    Sim2 = CosSim(linkidf1,linkidf2)
    alpha = 0.5
    beta = 0.5
    return (alpha*Sim1 + beta*Sim2)

def artcatsimilarity(category,article2):
    #Tfidf1 = TfIdf(category.content)
    #Tfidf2 = TfIdf(article2.content)

    Sim1 = CosSim(category.contentTfidf,article2.contentTfidf)
    return Sim1
