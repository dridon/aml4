#from sklearn import neighbors
import books as bks
import csv
import numpy as np
import math
from sklearn import svm
from sklearn import preprocessing as pp

numFolds = 4

def circInfo(data, threshold):
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

def calcThreshold(trainSet, form="median"):
    cvalues = np.array([ b.circ for b in trainSet ]) 
    avg = np.average(cvalues)
    median = np.median(cvalues)
    return avg if form == "avg" else median
    
def splitData(loans, fold, wordvecs = None):
  trainSet = []
  validSet =[]
  i = 0 
  for book in loans:
      i = i + 1
      if i%numFolds != fold:
          trainSet.append(book)
      else:
          validSet.append(book)
  threshold = calcThreshold(trainSet)
  authDict = circInfo(trainSet, threshold)

  trainX = []
  trainY = []
  validX = []
  validY = []
  for book in trainSet:
      if book.author[0] == '':
          circ = [0,0]
      else:
          circ = authDict[book.author]

      if wordvecs is None: 
        trainX.append([book.callno,book.year])
      else: 
        trainX.append([book.callno,book.year] + wordvecs(book.deweyVectors))

      if book.circ > threshold:
          trainY.append(1)
      else:
          trainY.append(0)

  for book in validSet:
      if book.author in authDict:
          circ = authDict[book.author]
      else:
          circ = [0,0]
      if wordvecs is None: 
        validX.append([book.callno,book.year])
      else: 
        validX.append([book.callno,book.year] + wordvecs(book.deweyVectors))

      if book.circ > threshold:
          validY.append(1)
      else:
          validY.append(0)

  return (trainX, trainY, validX, validY, threshold, authDict)

def splitDataTest(loans, limit, wordvecs = None):
  trainSet = loans[:limit]
  validSet = loans[limit+1:]
  threshold = calcThreshold(trainSet)
  authDict = circInfo(trainSet, threshold)

  trainX = []
  trainY = []
  validX = []
  validY = []
  for book in trainSet:
      if book.author[0] == '':
          circ = [0,0]
      else:
          circ = authDict[book.author]

      if wordvecs is None: 
        trainX.append([book.callno,book.year])
      else: 
        trainX.append([book.callno,book.year] + wordvecs(book.deweyVectors))

      if book.circ > threshold:
          trainY.append(1)
      else:
          trainY.append(0)

  for book in validSet:
      if book.author in authDict:
          circ = authDict[book.author]
      else:
          circ = [0,0]
      if wordvecs is None: 
        validX.append([book.callno,book.year])
      else: 
        validX.append([book.callno,book.year] + wordvecs(book.deweyVectors))

      if book.circ > threshold:
          validY.append(1)
      else:
          validY.append(0)

  return (trainX, trainY, validX, validY, threshold, authDict)

def wordVecSums(vecs):
  sumVec = np.zeros(vecs[0].shape[0])
  for v in vecs: 
    sumVec = np.add(sumVec, v)
  return list(sumVec)

def first4(vecs): 
  allVecs = (vecs * int(math.ceil((4.0/len(vecs)))))[:4] if len(vecs) < 4 else vecs[:4]
  return [ x for v in allVecs for x in list(v)] 

def runClassifier(classifier, trainX = [], trainY= [], validX= [], validY= []):
  success = 0
  failure = 0
  results=[]
  truePos = 0
  trueNeg = 0
  totPos = 0
  totNeg = 0
  classifier.fit(trainX, trainY)
  for i in range(len(validX)):
      if validY[i]==1:
          totPos += 1
      else:
          totNeg += 1
      Z=classifier.predict(validX[i])
      results.append((Z,validY[i],Z==validY[i]))
      if Z==validY[i]:
          success = success + 1
          if validY[i] == 1:
              truePos += 1
          else:
              trueNeg += 1
      else:
          failure = failure + 1
          

  return (float(success)/(success+failure), truePos/float(totPos), trueNeg/float(totNeg),results)

if __name__ == "__main__":
  libraries = [ l[0] for l in csv.reader(open("library_list2.csv", "r"))] 
  books = bks.Books(noWordVecs = True) 
  mms = pp.MinMaxScaler(copy = False)


  for l in libraries: 
    loans = (books.libraryLoans(l)).values()
    limit = int(round(0.8*len(loans)))
    train = loans[:limit]
    test = loans[limit+1:]
    threshold = None
    authDict = None

    ks = ['linear', 'rbf', 'sigmoid', 'poly']
    cs = [0.05, 0.5, 1.0, 2.5, 5.0]
    wvs = [None]
    for k in ks:
      for c in cs:
        for wv in wvs: 
          wvName = wv.__name__  if wv is not None else "None"
          success=[]
          sens = []
          spec = []
          # 10 fold validation
          for fold in range(4):
            """
              You can pass wordVecSums to get an extra feature set of 300 appended to it that sums all the word vectors OR 
              You can pass first4 that gets the first 4 vectors, if there are less than 4 vectors, it duplicates the entries till there are 4, 
              there will be a total of 1200 new features added as a result
            """
            trainX, trainY, validX, validY, threshold, authDict = splitData(train, fold, wordvecs = wv)
            trainX = mms.fit_transform(trainX) 
            validX = mms.fit_transform(validX)

            clfType = "SVM"
            classifier = svm.SVC(C = c, kernel = k, tol = 0.1)
            success_rate, sensitivity,specificity,results = runClassifier(
                classifier,
                trainX = trainX, 
                trainY = trainY, 
                validX = validX, 
                validY = validY) 
            success.append(success_rate)
            sens.append(sensitivity)
            spec.append(specificity)
          
            with open(clfType+'_results/'+'results_'+l[:9] +"_"+ k + "_" + str(c) + "_" + str(fold)+  '.csv','w') as csvfile:
              writer = csv.writer(csvfile,delimiter = ',', quotechar='\"', quoting=csv.QUOTE_ALL)
              for r in results:
                writer.writerow(r)
          print str(l) + "," + str(k) + "," + str(c) + "," + wvName + "," + str(round(np.average(success), 3)) + "," + str(round(np.average(sens), 3)) + "," + str(round(np.average(specificity), 3))


  """
  Generate test results
  """

  libraries = [ l[0] for l in csv.reader(open("library_list.csv", "r"))] 
  books = bks.Books(noWordVecs = True) 
  mms = pp.MinMaxScaler(copy = False)


  for l in libraries: 
    loans = (books.libraryLoans(l)).values()
    limit = int(round(0.8*len(loans)))
    threshold = None
    authDict = None

    success=[]
    sens = []
    spec = []
    trainX, trainY, validX, validY, threshold, authDict = splitDataTest(loans, limit, wordvecs = None)
    trainX = mms.fit_transform(trainX) 
    validX = mms.fit_transform(validX)

    clfType = "SVM"
    classifier = svm.SVC(C = 0.5, kernel = 'rbf', tol = 0.1)
    success_rate, sensitivity,specificity,results = runClassifier(
        classifier,
        trainX = trainX, 
        trainY = trainY, 
        validX = validX, 
        validY = validY) 
    success.append(success_rate)
    sens.append(sensitivity)
    spec.append(specificity)
          
    with open(clfType+'_results/final_'+l+"_svm_results"+'.csv','w') as csvfile:
      writer = csv.writer(csvfile,delimiter = ',', quotechar='\"', quoting=csv.QUOTE_ALL)
      for r in results:
        writer.writerow(r)
    print str(l) + ","+ str(round(np.average(success), 3)) + "," + str(round(np.average(sens), 3)) + "," + str(round(np.average(specificity), 3))
