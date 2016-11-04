import wikipedia
import re
from collections import Counter
import operator
from categories import *;

DEPTH = 2;

stopListSmall = ["a","an","and","are","as","at","be","by","for","from","has","he","in","is","it","its","of","on","or","that","the","to","was","were","will","with",""];

stopListBig = ["a","as","able","about","above","according","accordingly","across","actually","after","afterwards","again","against","aint","all","allow","allows","almost","alone","along","already","also","although","always","am","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anyways","anywhere","apart","appear","appreciate","appropriate","are","arent","around","as","aside","ask","asking","associated","at","available","away","awfully","b","be","became","because","become","becomes","becoming","been","before","beforehand","behind","being","believe","below","beside","besides","best","better","between","beyond","both","brief","but","by","c","cmon","cs","came","can","cant","cannot","cant","cause","causes","certain","certainly","changes","clearly","co","com","come","comes","concerning","consequently","consider","considering","contain","containing","contains","corresponding","could","couldnt","course","currently","d","definitely","described","despite","did","didnt","different","do","does","doesnt","doing","dont","done","down","downwards","during","e","each","edu","eg","eight","either","else","elsewhere","enough","entirely","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","exactly","example","except","f","far","few","fifth","first","five","followed","following","follows","for","former","formerly","forth","four","from","further","furthermore","g","get","gets","getting","given","gives","go","goes","going","gone","got","gotten","greetings","h","had","hadnt","happens","hardly","has","hasnt","have","havent","having","he","hes","hello","help","hence","her","here","heres","hereafter","hereby","herein","hereupon","hers","herself","hi","him","himself","his","hither","hopefully","how","howbeit","however","i","id","ill","im","ive","ie","if","ignored","immediate","in","inasmuch","inc","indeed","indicate","indicated","indicates","inner","insofar","instead","into","inward","is","isnt","it","itd","itll","its","its","itself","j","just","k","keep","keeps","kept","know","knows","known","l","last","lately","later","latter","latterly","least","less","lest","let","lets","like","liked","likely","little","look","looking","looks","ltd","m","mainly","many","may","maybe","me","mean","meanwhile","merely","might","more","moreover","most","mostly","much","must","my","myself","n","name","namely","nd","near","nearly","necessary","need","needs","neither","never","nevertheless","new","next","nine","no","nobody","non","none","noone","nor","normally","not","nothing","novel","now","nowhere","o","obviously","of","off","often","oh","ok","okay","old","on","once","one","ones","only","onto","or","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","overall","own","p","particular","particularly","per","perhaps","placed","please","plus","possible","presumably","probably","provides","q","que","quite","qv","r","rather","rd","re","really","reasonably","regarding","regardless","regards","relatively","respectively","right","s","said","same","saw","say","saying","says","second","secondly","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","she","should","shouldnt","since","six","so","some","somebody","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still","sub","such","sup","sure","t","ts","take","taken","tell","tends","th","than","thank","thanks","thanx","that","thats","thats","the","their","theirs","them","themselves","then","thence","there","theres","thereafter","thereby","therefore","therein","theres","thereupon","these","they","theyd","theyll","theyre","theyve","think","third","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","to","together","too","took","toward","towards","tried","tries","truly","try","trying","twice","two","u","un","under","unfortunately","unless","unlikely","until","unto","up","upon","us","use","used","useful","uses","using","usually","uucp","v","value","various","very","via","viz","vs","w","want","wants","was","wasnt","way","we","wed","well","were","weve","welcome","well","went","were","werent","what","whats","whatever","when","whence","whenever","where","wheres","whereafter","whereas","whereby","wherein","whereupon","wherever","whether","which","while","whither","who","whos","whoever","whole","whom","whose","why","will","willing","wish","with","within","without","wont","wonder","would","would","wouldnt","x","y","yes","yet","you","youd","youll","youre","youve","your","yours","yourself","yourselves","z","zero"
,""];

def giveContent(article):
    page = wikipedia.page(article);
    content = page.content;
    # content = content.decode('utf-8').encode('ascii','xmlcharrefreplace');
    content = content.lower();
    content = re.sub('[!@#$%&()\n=\'\",.]*','',content);
    content = re.sub('[0-9]*','',content);
    # print content;
    # content = re.sub('\\\u[0-9]*','',content);
    # words = map(str,content.split(" "));
    words = [];
    for w in content.split(" "):
        try:
            words.append(str(w));
        except UnicodeEncodeError:
            pass
        # print str(w);
    print len(words);
    words = [w for w in words if w not in stopListBig];
    print len(words);
    return words;

def giveSummary(article):
    summry = wikipedia.summary(article);
    return summry;

def pruneCategories(article):
    categories = giveCategories();  # TODO by rajiv
    simDict = {};
    for catgry in categories:
        simDict[catgry] = simArtclCtgry(article,catgry);
    sortedList = sorted(simDict.items(),key=operator.itemgetter(1));
    return sortedList[:2];

def simArtclCtgry(article,catgry):
    catgryPage = wikipedia.page("category:"+catgry);
    catgryArtclsList = catgryPage.links;
    if "category" in catgryArtclsList:
        catgryArtclsList.remove("category");
    catgrySimSum = 0;
    for catgryArtcls in catgryArtclsList:
        catgrySimSum += articleSimlarity(article,catgryArtcls); # TODO by sahiti
    return catgrySimSum/len(catgryArtclsList);

def pruneArticles(article,catgry,thrshld):
    artclList = giveArticles(DEPTH,catgry)[1];     # DONE by hemanth
    artclDict = {};
    for catgryArtcl in artclList:
        artclDict[catgryArtcl] = articleSimlarity(article,catgryArtcl);
    sortedList = sorted(artclDict.items(),key=operator.itemgetter(1));
    filterList = [x for (x,y) in sortedList if y > thrshld];
    return filterList;

t = giveContent("india")
