# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 14:52:22 2014

@author: Fernando Sa-Pereira
"""
import csv, re
threshold = 3

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

def circInfo(data):
    authDict = {}
    for d in data:
        if d.author[0] != '':
            if d.author in authDict:
                authCounts = authDict[d.author]
            else:
                authCounts = [0,0]        
                
            if d.circ >= threshold:
                authCounts[0] = authCounts[0]+1
            else:
                authCounts[1] = authCounts[1]+1

            authDict[d.author] = authCounts
            
    return authDict
    
def loadStops(filename):
    """
    stop words list source: http://www.textfixer.com/resources/common-english-words.txt
                            http://www.ranks.nl/stopwords/french
    """
    stopwords = set()

    with open(filename,'rb') as stopwordfile:
        datareader = csv.reader(stopwordfile)
        for w in datareader:
            stopwords.update(w)
            
    stopwordfile.close()
    
    return stopwords
    
def reduce(theString,wordset):
    words = theString.split(" ")
    newString = []
    for w in words:
        w=w.lower()        
        if w not in wordset:
          w = re.sub(r"[^\w\s\']",'',w)
          if re.search('[0-9]',w) == None and w != '':
              newString.append(w)  
    
    return newString

"""
stopword list source: http://www.textfixer.com/resources/common-english-words.txt
"""
stopwords = [loadStops('eng-stopwords.csv'), loadStops('fr-stopwords.csv')]

skipped = 0
dupl = 0
exc=[0,0,0]

loans = {}

with open('nonfiction-no-accents.csv','rb') as infile:
    datareader = csv.reader(infile)
    for record in datareader:
       if record[0] == "Sans Arroundissement": 
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
           
                title = reduce(record[8],stopwords[lang])
                title = title + reduce(record[9],stopwords[lang])
 
                if not skipflag:
                    book = Book()
                    bookkey=(callno,author,year,lang)
                    if bookkey in loans:
                        loans[bookkey].circ = loans[bookkey].circ + circ
                        dupl = dupl +1
                    else:
                        book.callno = callno
                        book.circ = circ
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
print 'duplicate books ',dupl 
print 'unique books ', len(loans) 

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
    
    authDict = circInfo(trainSet)
    
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
        
    from sklearn import neighbors
    n_neighbors = 20
    
    clf = neighbors.KNeighborsClassifier(n_neighbors, weights='distance')
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
    for i in range(len(x)):
        Z=clf.predict(x[i])
        results.append((x[i],Z,y[i],Z==y[i]))
        if Z==y[i]:
            success = success + 1
        else:
            failure = failure + 1
    print float(success)/(success+failure)
    with open('results'+'{}'.format(m)+'.csv','w') as csvfile:
        writer = csv.writer(csvfile,delimiter = ',', quotechar='\"', quoting=csv.QUOTE_ALL)
        for r in results:
            writer.writerow(r)
    csvfile.close()