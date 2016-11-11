'''
Created on 10-Nov-2016

@author: hemanth

'''
import requests;
import time;

start = time.time();

EASY_ESA = "http://vmdeb20.deri.ie:8890/esaservice";
esaArt1 = {'task':'vector', 'source': 'tomasulo algorithm', 'limit':'50'};
esaArt2 = {'task':'vector', 'source': 'instruciton level parallelism', 'limit':'50'};
esaParams = {'task':'esa', 'term1':'tomasulo algorithm', 'term2':'instruction level parallelism'};

resp = requests.get(EASY_ESA, esaArt1);
print resp.text;
resp = requests.get(EASY_ESA, esaArt2);
print resp.text;
resp = requests.get(EASY_ESA, esaParams);
print resp.text;

end = time.time();
print "time taken: "+str(end-start);
