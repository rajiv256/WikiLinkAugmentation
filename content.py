import wikipedia
import re

stopList = ["a","an","and","are","as","at","be","by","for","from","has","he","in","is","it","its","of","on","that","the","to","was","were","will","with",""];

def giveContent(article):
    page = wikipedia.page(article);
    content = page.content;
    # content = content.decode('utf-8').encode('ascii','xmlcharrefreplace');
    content = content.lower();
    content = re.sub('[!@#$%&()\n=\',.]*','',content);
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
    words = [w for w in words if w not in stopList];
    print len(words);
    return words;

t = giveContent("india")
