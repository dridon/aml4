# -*- coding: utf-8 -*-
"""
Adaptation of Fernando's Code to make it re-usable
"""
import csv, re
from dewey_dict import DeweyCode 
from wordvectors import Word2Vec
 

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

def get_vectors(word2vec, words): 
  vectors = [] 
  for w in words:
    v = word2vec.get_vector(w, verbose = False)
    if v is not None: vectors.append(v)
  return vectors

class Books: 
  stopwords = None
  deweyCode = None
  wv = None
  dataf = ""
  cache = {}

  def __init__(self, 
      dataFile = "nonfiction-no-accents.csv",
      englishStopWordsFile = 'eng-stopwords.csv', 
      frenchStopWordsFile = 'fr-stopwords.csv', 
      deweyDictFile = "dewey_dictionary.csv", 
      wordvecFile="GoogleNews-vectors-negative300.bin"): 

    self.dataf = dataFile
    self.stopwords = [loadStops(englishStopWordsFile), loadStops(frenchStopWordsFile)]

    # # initialize Dewey conversion
    self.deweyCode = DeweyCode(deweyDictFile)

    # #initializes word vectors
    self.wv = Word2Vec(wordvecFile)

  def libraryLoans(self, library):
    if library in self.cache: return self.cache[library] 

    print "Processing book loans for " + library

    skipped = 0
    dupl = 0
    loans = {}
    exc=[0,0,0]
    f = open(self.dataf, 'rb')
    datareader = csv.reader(f)
    for record in datareader:
       if record[0] == library: 
            skipflag = False

            callno = re.match('\D*([\d\.]*)',record[7]).group(1)
            deweyClasses = None   
            if callno != '':
                try:
                    deweyClasses = self.deweyCode.dewey_classes_extract(callno)
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
       
            title = reduce(record[8],self.stopwords[lang])
            title = title + reduce(record[9],self.stopwords[lang])

            # Convert word lists to word vectors
            deweyWords = list({word for s in deweyClasses[1] for word in reduce(s, self.stopwords[lang]) if s is not None}) if deweyClasses is not None else deweyClasses
            deweyVectors = get_vectors(self.wv, deweyWords) if deweyWords is not None else None
            titleVectors = get_vectors(self.wv, title) if title is not None else None

            if not skipflag:
                book = Book()
                bookkey=(callno,author,year,lang)
                if bookkey in loans:
                    loans[bookkey].circ = loans[bookkey].circ + float(circ)/(2014-year + 1)
                    dupl = dupl +1
                else:
                    book.callno = callno
                    book.circ = float(circ)/(2014-year + 1 )
                    book.author = author
                    book.title = title
                    book.year = year
                    book.pages = pages
                    book.lang = lang
                    book.isbn = record[18]

                    book.deweyClasses = deweyClasses
                    book.deweyWords = deweyWords
                    book.deweyVectors = deweyVectors
                    book.titleVectors = titleVectors
                    loans[bookkey]=book                  
            else:
                skipped = skipped + 1 
    # caching abandoned because it uses too much memory for all libraries
    # self.cache[library] = loans
    f.close()
    return loans

if __name__ == "__main__":
  books = Books()
  slBooks = books.libraryLoans("Saint-Laurent") 
