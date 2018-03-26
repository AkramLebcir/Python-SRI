from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from search.models import Documment,Mot,MotCol,FilInverse,ChartDoc
from django.views import View
import nltk
from nltk.tokenize import word_tokenize
import math
import threading
# from chartit import DataPool, Chart



class Detail(View):
    def get(self,request,docum,*args,**kwargs):
        
        try:
            print(int(docum))
            filinverses = FilInverse.objects.fields(documents=int(docum))
            
            return render(request,'detail.html',{'docum':filinverses[0].documents[int(docum)]})
        except :
            filinverses = "documment !!"
            return render(request,'detail.html',{'docum':filinverses})
        

class Index(View):
    
    def get(self,request,*args,**kwargs):
        filinverses=[]
        #nltk.download('punkt')
        
        return render(request,'index.html',{'filinverses':filinverses})
    
    
    def post(self,request,*args,**kwargs):
        filinverses=[]
        
        caractere = [",",".",":",";",">","<","-","_","+","=","(",")","*","&","^","%","$","#","@","[","]","}","{","|","'","\"","?","!","/","``"]
        if request.POST.get("rq"):
            if request.POST.get("rq")!=" ":
                #nltk.download('punkt')
                mots = []
                cols = []
                collocword = []
                filinverses = FilInverse.objects
                stoplist = filinverses[0].stopConcepts
                documents = filinverses[0].documents
                N = len(documents)
                boolien = False
                rqtoken = word_tokenize(request.POST.get("rq"))
                rqtoken = [s.lower() for s in rqtoken if s not in caractere] 
                for l,word in enumerate(rqtoken):              
                    collocword[:] = []
                    collocs = filinverses[0].filinverse.cols[:]
                    for w in collocs:
                        if w.nomMot.find(word.lower()+" ") == 0:
                            collocword.append(w)
                    while (boolien == False) and (collocword):
                        collocword.sort(key=len)
                        collocC = collocword.pop()
                        lenth = len(word_tokenize(collocC.nomMot))
                        collocE = ' '.join(rqtoken[l:l+lenth]).lower()
                        if (collocC.nomMot == collocE):
                            boolien = True
                            break

                    if (boolien == True):
                        boolien = False
                        colloc = Mot()
                        colloc.nomMot = collocC
                        colloc.nbrDoc = 1
                        doc = Documment()
                        doc.nomDoc = -1                            
                        doc.nbrFreq = rqtoken.count(collocC)
                        colloc.docs = [doc]
                        cols.append(colloc)
                    else:
                        if word.lower() not in stoplist:
                            wor = word.lower()
                            mot = Mot()
                            mot.nomMot = wor
                            mot.nbrDoc = 1
                            doc = Documment()
                            doc.nomDoc = -1                            
                            doc.nbrFreq = rqtoken.count(wor)
                            mot.docs = [doc]
                            mots.append(mot)

                motsdb = filinverses[0].filinverse.mots[:]
                colsdb = filinverses[0].filinverse.cols[:]
                
                indexmots = []
                indexmotsdb = []
                indexcols = []
                indexcolsdb = []

                def fun():
                    for motdb in motsdb:
                        if mot.nomMot == motdb.nomMot:
                            indexmots.append(mot)
                            indexmotsdb.append(motdb)

                for mot in mots:
                    t = threading.Thread(name='save',target=fun)
                    t.start()

                def fun2():
                    for coldb in colsdb:
                        if col.nomMot == coldb.nomMot:
                            indexcols.append(col)
                            indexcolsdb.append(coldb)
                            
                for col in cols:
                    t2 = threading.Thread(name='save',target=fun2)
                    t2.start()
                    

                indexdb = indexmotsdb[:]+indexcolsdb[:]
                index = indexmots[:]+indexcols[:]
                m=float(0)
                m1=float(0)
                m2=float(0)
                multindex = [0.0] * N
                sumindex = [0.0] * N

                def nbrdocthre():
                    m=float(0)
                    m1=float(0)
                    m2=float(0)
                    for j,indedb in enumerate(indexdb):
                        for k,doc in enumerate(indedb.docs):
                            if doc.nomDoc == i:
                                m += float(indedb.docs[k].nbrFreq)*float(index[j].docs[0].nbrFreq)
                                m1 += float(index[j].docs[0].nbrFreq)*float(index[j].docs[0].nbrFreq)
                                m2 += float(indedb.docs[k].nbrFreq)*float(indedb.docs[k].nbrFreq)
                    multindex[i] = m
                    sumindex[i] = m1 + m2

                for i in range(N):
                    if i < N-2:
                        t3 = threading.Thread(name='save',target=nbrdocthre)
                        t3.start()
                    else:
                        m=float(0)
                        m1=float(0)
                        m2=float(0)
                        for j,indedb in enumerate(indexdb):
                            for k,doc in enumerate(indedb.docs):
                                if doc.nomDoc == i:
                                    m += float(indedb.docs[k].nbrFreq)*float(index[j].docs[0].nbrFreq)
                                    m1 += float(index[j].docs[0].nbrFreq)*float(index[j].docs[0].nbrFreq)
                                    m2 += float(indedb.docs[k].nbrFreq)*float(indedb.docs[k].nbrFreq)
                        multindex[i] = m
                        sumindex[i] = m1 + m2

                    
                scores = [0.0] * N
                
                for i,x in enumerate(multindex):
                    if (sumindex[i]-x) != 0.0:
                        scores[i] = ((2*x)/(sumindex[i]-x))
                    else:
                        scores[i] = 0.0
                docpert = []
                
                scorenew = []
                indexdoc = []
                for i,doc in enumerate(documents):
                    if scores[i] > 0.0:
                        docpert.append(doc)
                        scorenew.append(scores[i])
                        indexdoc.append(i)
                
                docpert2 = sorted(zip(scorenew,docpert,indexdoc), key=lambda x: x[0])

                f = []
                try:
                    x2, y2,z2 = zip(*docpert2)
                    for score,inde in zip(x2,z2):
                        t = [inde,score]
                        f.append(t)
                except :
                    filinverses=[]
                    return render(request,'index.html',{'filinverses':filinverses})
              
                return render(request,'index.html',{'filinverses':zip(z2,y2),'chartdata':list(f),'indexdb':index})

        return render(request,'index.html',{'filinverses':filinverses})