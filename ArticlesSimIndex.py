'''
Article : (content ,summary , hyperlinks, see also, Categories)

'''

from tfidf import *


def similarity(article1,article2):
    Tfidf1 = TfIdf(article1.summary)
    Tfidf2 = TfIdf(article2.summary)

    Sim1 = CosSim(Tfidf1,Tfidf2)
    links1 = map(lambda p : p[0] ,article1.summaryhyperlinks())
    links2 = map(lambda p: p[0], article2.summaryhyperlinks())

    linkidf1 = linkTfIdf(links1)
    linkidf2 = linkTfIdf(links2)
    Sim2 = CosSim(linkidf1,linkidf2)
    alpha = 0.5
    beta = 0.5
    return (alpha*Sim1 + beta*Sim2)

def artcatsimilarity(category,article2):
    Tfidf1 = TfIdf(category.content)
    Tfidf2 = TfIdf(article2.content)

    Sim1 = CosSim(Tfidf1,Tfidf2)
    return Sim1
