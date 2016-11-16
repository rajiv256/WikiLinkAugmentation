import pickle;
final = pickle.load(open('Allhtmls_short0.5.pkl','r'));
print 0.5,len(final);
for i in range(0,7):
    t = pickle.load(open('Allhtmls_short'+str(i)+'.pkl','r'));
    print i, len(t);
    final += t;

pickle.dump(final,open('Allhtmls.pkl','w'))
