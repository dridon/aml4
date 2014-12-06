from sklearn import neighbors
import books as bks
import csv
import numpy as np

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

def calcThreshold(trainSet, form="avg"):
    cvalues = np.array([ b.circ for b in trainSet ]) 
    avg = np.average(cvalues)
    median = np.median(cvalues)
    stdev = np.std(cvalues)
    if form == "avg":
        return avg,stdev 
    else: 
        return median,stdev
    
def encodeOutput(n,threshold,stdev):
    output = 0
    if n > 0 and n < threshold:
        output = 1
    if n >= threshold and n < (threshold + stdev):
        output = 2
    if n >= (threshold + stdev):
        output = 3

    return output

def splitData(loans, fold):
  trainSet = []
  testSet =[]

  i = 0 
  for book in loans.values():
      i = i + 1
      if i%10 != fold:
          trainSet.append(book)
      else:
          testSet.append(book)
  threshold,stddev = calcThreshold(trainSet)
  authDict = circInfo(trainSet, threshold)

  trainX = []
  trainY = []
  testX = []
  testY = []
  for book in trainSet:
      if book.author[0] == '':
          circ = [0,0]
      else:
          circ = authDict[book.author]
      trainX.append([book.callno,circ[0],circ[1],book.year, book.lang])
      trainY.append(encodeOutput(book.circ,threshold,stddev))
          
  for book in testSet:
      if book.author in authDict:
          circ = authDict[book.author]
      else:
          circ = [0,0]
      testX.append([book.callno,circ[0],circ[1],book.year, book.lang])
      testY.append(encodeOutput(book.circ,threshold,stddev))

  return (trainX, trainY, testX, testY, threshold,stddev)

def runClassifier(classifier, trainX = [], trainY= [], testX= [], testY= []):
  success = 0
  failure = 0
  results=[]

  classifier.fit(trainX, trainY)
  for i in range(len(testX)):
      Z=classifier.predict(testX[i])
      results.append((testX[i],Z,testY[i],Z==testY[i]))
      if Z==testY[i]:
          success = success + 1
      else:
          failure = failure + 1

  return (float(success)/(success+failure), results)
  

if __name__ == "__main__":
  libraries = [ l[0] for l in csv.reader(open("library_list.csv", "r"))] 
  books = bks.Books() 

  # run KNN
  for l in libraries: 
    loans = books.libraryLoans(l)

    # 10 fold validation
    for fold in range(10):
      trainX, trainY, testX, testY, threshold, stddev = splitData(loans, fold)
      from sklearn.svm import SVC
      clfType = "SVM"
      classifier = SVC()
      
      success_rate, results = runClassifier(
          classifier,
          trainX = trainX, 
          trainY = trainY, 
          testX = testX, 
          testY = testY) 
          
      print "Library " + str(l[:8]) + " fold " + str(fold) + " with threshold " + str(threshold) + " and std dev " + str(stddev)+ " sucecss rate is " + str(success_rate)
      with open(clfType+' results/'+'results '+l[:9] + "_fold_" + str(fold)  + '.csv','w') as csvfile:
        writer = csv.writer(csvfile,delimiter = ',', quotechar='\"', quoting=csv.QUOTE_ALL)
        for r in results:
          writer.writerow(r)
