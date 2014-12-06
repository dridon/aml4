# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 14:52:22 2014

@author: Fernando Sa-Pereira
"""
import csv, re
import numpy as np
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.metrics import confusion_matrix
from sklearn import svm, datasets
import matplotlib.pyplot as plt

class Book: pass

def authorInfo(fullname):
    authKey = None
    names = fullname.split(',')
    
    if len(names) >= 1:
        lastname = names[0]
    if len(names) >1:
        firstname = names[1]
    else:
        firstname = None
    #other names are ignored
    
    authKey = (lastname,firstname)
    return authKey

def circInfo(data, threshold):
    authDict = {}
    maxPos = 0
    maxNeg = 0
    for d in data:
        if d.author[0] != '':
            if d.author in authDict:
                authCounts = authDict[d.author]
            else:
                authCounts = [0,0]        
                
            if d.circ >= threshold:
                authCounts[0] = authCounts[0]+1
                if maxPos < authCounts[0]:
                    maxPos = authCounts[0]
            else:
                authCounts[1] = authCounts[1]+1
                if maxNeg < authCounts[1]:
                    maxNeg = authCounts[1]

            authDict[d.author] = authCounts
            
    return authDict,maxPos,maxNeg
    
def calcThreshold(trainSet, form="avg"):
    cvalues = np.array([ b.circ for b in trainSet ]) 
    avg = np.average(cvalues)
    median = np.median(cvalues)
    return avg if form == "avg" else median
    
def normalize(dataset,maxPos,maxNeg):
    norm = []
    maxPos = float(maxPos)
    maxNeg = float(maxNeg)    
    for d in dataset:
        norm.append([d[0]/1000.0,d[1]/maxPos,d[2]/maxNeg,d[3]/2014,d[4]])
    return norm
    
skipped = 0
exc=[0,0,0]

for library in ["Saint-Laurent","Plateau-Mont-Royal","Saint-Leonard",\
                "Outremont","Anjou","Mercier-Hochelaga-Maisonneuve","Verdun",\
                "Sans Arroundissement"]:
    loans = {}
    print "Results for ",library
    with open('nonfiction-no-accents.csv','rb') as infile:
        datareader = csv.reader(infile)
        for record in datareader:
                skipflag = False
            
                callno = re.match('\D*([\d\.]*)',record[7]).group(1)
                if callno != '':
                    try:
                        callno = float(callno)
                    except ValueError:
                        callno = 0
                        skipFlag = True
                else:
                    exc[0]=exc[0]+1
                    skipflag = True 

                circ = int(record[3])
                
                title = record[8]

                author = authorInfo(record[10])
                if author == None:
                    exc[1]=exc[1]+1
                    skipflag = True 
           
                m=re.search("\D*(\d{4})",record[15])
                if record[15] != '':
                    if m == None or m.group(1) == '':
                        exc[2]=exc[2]+1
                        skipflag = True 
                    else:
                        year = int(m.group(1))
                
                p = re.search("\D*(\d*)\D*",record[16])
                if p != None and p.group(1) != '':
                    pages = int(p.group(1))
                    
                if record[17] == 'eng':
                    lang = 0
                elif record[17] == 'fre':
                    lang = 1
                else:
                    skipflag = True 
                
                if not skipflag:
                    book = Book()
                    bookkey=(callno,author,year,lang)
                    if bookkey in loans:
                        loans[bookkey].circ = loans[bookkey].circ + float(circ)/(2014-year + 1)
                    else:
                        book.callno = callno
                        book.circ = float(circ)/(2014-year + 1 )
                        book.author = author
                        book.title = title
                        book.year = year
                        book.pages = pages
                        book.lang = lang
                        book.isbn = record[18]
                        loans[bookkey]=book
                else:
                    skipped = skipped + 1 
                                   
                
    infile.close()
    print skipped, exc 
    
    for m in range(10):
        i = 0
        trainSet = []
        testSet =[]
        for book in loans.values():
            i = i + 1
            if i % 10 != m:
                trainSet.append(book)
            else:
                testSet.append(book)
                
        threshold = calcThreshold(trainSet)
        authDict,maxPos,maxNeg = circInfo(trainSet,threshold)
        
        x = []
        y = []
        for book in trainSet:
            if book.author[0] == '':
                circ = [0,0]
            else:
                circ = authDict[book.author]
            x.append([book.callno,circ[0], circ[1],book.year,book.lang])
            if book.circ > threshold:
                y.append(1)
            else:
                y.append(0)
            
        
        clf = BernoulliNB()
        clf.fit(x, y)
        
        x=[]
        y=[]
        for book in testSet:
            if book.author in authDict:
                circ = authDict[book.author]
            else:
                circ = [0,0]
            x.append([book.callno,circ[0], circ[1],book.year,book.lang])
            if book.circ > threshold:
                y.append(1)
            else:
                y.append(0)
        
        success = 0
        failure = 0
        results=[]
       
        Z=clf.predict(x)
        
        for i in range(len(x)):
            if Z[i]==y[i]:
                success = success + 1
            else:
                failure = failure + 1
        print float(success)/(success+failure)
        
    
    
        cm = confusion_matrix(y, Z)
        print(cm)
        plt.matshow(cm)
        plt.title('Confusion matrix')
        plt.colorbar()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.show()
