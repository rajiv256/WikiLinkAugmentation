'''
Article : (content ,summary , hyperlinks, see also, Categories)

'''
import ArticleClass
from tfidf import *
from parser import *

def articleSimilarity(article1,article2):
    # print "article1 : "
    # print article1.title
    # print "article2 : "
    # print article2.title
    Tfidf1 = article1.contentTfIdf
    Tfidf2 = article2.contentTfIdf
    ConceptSim = ConceptVectorSimilarity(Tfidf1,Tfidf2)
    Sim1 = CosSim(article1.summryTfIdf,article2.summryTfIdf)
    #forget summary hyperlinks for now ,it is not working.
    '''
    if(article1.summaryhyperlinks == []):
        print "going inside"
        article1 = fill_links(article1)
    if(article2.summaryhyperlinks == []):
        print "going indise 2 "
        article2 = fill_links(article2)
    links1 = map(lambda p: p[0] ,article1.summaryhyperlinks)
    links2 = map(lambda p: p[0], article2.summaryhyperlinks)
    linkidf1 = linkTfIdf(links1)
    linkidf2 = linkTfIdf(links2)
    print linkidf1
    print linkidf2
    Sim2 = CosSim(linkidf1,linkidf2)
    alpha = 0.5
    beta = 0.5
    return (alpha*Sim1 + beta*Sim2)
    '''
    return (Sim1,ConceptSim)

def artcatsimilarity(category,article2):
    #Tfidf1 = TfIdf(category.content)
    #Tfidf2 = TfIdf(article2.content)

    Sim1 = ConceptVectorSimilarity(category.contentTfIdf,article2.contentTfIdf)
    return Sim1

def hyperlinksimilarity(article1,article2):
    article1 = fill_links(article1)
    article2 = fill_links(article2)
    artcl1Anchors = map(lambda p : p[0] , article1.hyperlinks)
    artcl2Anchors = map(lambda p : p[0] , article2.hyperlinks)

    # print "article 1 anchors"
    # print artcl1Anchors
    # print "article 2 anchors"
    # print artcl2Anchors
    #print len(set(artcl1Anchors)&set(artcl2Anchors))
    #print len(set(artcl1Anchors)|set(artcl2Anchors))
    if(len(set(artcl1Anchors)|set(artcl2Anchors))  == 0):
        return 0
    return len(set(artcl1Anchors)&set(artcl2Anchors))/float(len(set(artcl1Anchors)|set(artcl2Anchors)))
