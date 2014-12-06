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
    return avg if form == "avg" else median

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
  threshold = calcThreshold(trainSet)
  authDict = circInfo(trainSet, threshold)

  x = []
  y = []

  for book in trainSet:
      if book.author[0] == '':
          circ = [0,0]
      else:
          circ = authDict[book.author]
      x.append([book.callno,circ[0],circ[1],book.year, book.lang])
      if book.circ > threshold:
          y.append(1)
      else:
          y.append(0)
  trainX = x
  trainY = y

  x=[]
  y=[]
  for book in testSet:
      if book.author in authDict:
          circ = authDict[book.author]
      else:
          circ = [0,0]
      x.append([book.callno,circ[0],circ[1],book.year, book.lang])
      if book.circ > threshold:
          y.append(1)
      else:
          y.append(0)

  testX = x 
  testY = y 
  return (trainX, trainY, testX, testY, threshold)

def runKnn(n_neighbors = 20, threshold = 2, trainX = [], trainY= [], testX= [], testY= []):
  success = 0
  failure = 0
  results=[]

  clf = neighbors.KNeighborsClassifier(n_neighbors)
  clf.fit(trainX, trainY)
  for i in range(len(testX)):
      Z=clf.predict(testX[i])
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
  n_neighbors = 20
  for l in libraries: 
    loans = books.libraryLoans(l)

    # 10 fold validation
    for fold in range(10):
      trainX, trainY, testX, testY, threshold = splitData(loans, fold)
      success_rate, results = runKnn(
          threshold=threshold, 
          trainX = trainX, 
          trainY = trainY, 
          testX = testX, 
          testY = testY, 
          n_neighbors=n_neighbors)
      print "Library " + str(l) + " fold " + str(fold) + " with threshold " + str(threshold) + " sucecss rate is " + str(success_rate)
      with open('results/results_knn_library_'+'{}'.format(l.split()[0]) +"_neighbors_" + str(n_neighbors) + "_fold_" + str(fold)  + '.csv','w') as csvfile:
        writer = csv.writer(csvfile,delimiter = ',', quotechar='\"', quoting=csv.QUOTE_ALL)
        for r in results:
          writer.writerow(r)
