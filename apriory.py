import time as tt
t0=tt.time()
dats=[['google','amazon',],['amazon','google','python','cse'],['cse','google'],['amazon','python'],
      ['cse','amazon','python','google'],['amazon','google','cse','data',]]
sf=[]
from itertools import combinations
import pandas as pd
def pruned(it,k,l):
    subs=combinations(sorted(it),k)
    for itm in subs:
        if itm not in l:
            return False
    return True
def apriori_gen(c,data,minsp,k,l):
    C=[]
    for i in range(0,len(c)):
        itm=[]
        for j in range(i+1,len(c)):
            if c[i][0:(k-1)]==c[j][0:(k-1)]:
                if type(c[i][0:(k-1)])!=tuple:
                    itm=(c[i][0:(k-1)])+(c[i][(k-1)])+(c[j][(k-1)])
                else:
                    itm=c[i][0:(k-1)]+(c[i][(k-1)],)+(c[j][(k-1)],)
                itm=tuple(sorted(itm))
            if pruned(itm,k,l)!=False and itm not in C:
                C.append(itm)
                
    return C        
def apriori(data,minsp):
    global sf
    kdc={}
    fi,sfi=[],[]
    for dat in data:
        for i in range(0,len(dat)):
            if dat[i] not in kdc:
                kdc[dat[i]]=1
            elif dat[i] in dat[0:i]:
                continue
            else:
                kdc[dat[i]]+=1
    for k,v in kdc.items():
                if v>=minsp:
                    fi.append((k,v))
                    sfi.append(k)
    sfi=sorted(sfi)
    sf=fi
    for i in range(len(data)):
        data[i]=tuple(set(sfi).intersection(set(data[i])))
    k=2
    l=[]
    c=[]
    c=combinations(sfi,2)
    for it in c:
        l.append(it)
    c=l
    dic={}
    while len(l)!=0:
        if k>2:
            c=apriori_gen(l,dats,minsp,k-1,l)
        for it in data:
            sub=combinations(it,k)
            subs=[]
            for itms in sub:
                subs.append(tuple(sorted(itms)))
            for itm in c:
                itm=tuple(sorted(itm))
                if itm in subs:
                    #print(itm,"----",subs)
                    if itm not in dic:
                        dic[itm]=1
                    else:
                        dic[itm]+=1
        l=[]
        for key,v in dic.items():
            if v>=minsp:
                fi.append((key,v))
                l.append(key)
        dic={}
        k=k+1
    freq=fi
    data=pd.DataFrame(columns=["items","support"])
    its=[]
    sps=[]
    for i in range(0,len(freq)):
        its.append(str(freq[i][0]))
        sps.append(freq[i][1])
    data["items"]=its
    data["support"]=sps
    return data
import requests as rq
res=rq.get(r"https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/groceries.csv")
datass=[]
for it in res.iter_lines(1000000):
    li=[]
    for itm in it.split():
        li.append(itm)
    datass.append(li)
dii=datass[0:100]
print(apriori(dats,2).sort_values(ascending=False,by="support"))
