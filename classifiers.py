#from sklearn import neighbors
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
  validSet =[]
  i = 0 
  for book in loans:
      i = i + 1
      if i%10 != fold:
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
      trainX.append([book.callno,circ[0],circ[1],book.year, book.lang])
      if book.circ > threshold:
          trainY.append(1)
      else:
          trainY.append(0)
          
  for book in validSet:
      if book.author in authDict:
          circ = authDict[book.author]
      else:
          circ = [0,0]
      validX.append([book.callno,circ[0],circ[1],book.year, book.lang])
      if book.circ > threshold:
          validY.append(1)
      else:
          validY.append(0)

  return (trainX, trainY, validX, validY, threshold)

def runClassifier(classifier, trainX = [], trainY= [], validX= [], validY= []):
  success = 0
  failure = 0
  results=[]

  classifier.fit(trainX, trainY)
  for i in range(len(validX)):
      Z=classifier.predict(validX[i])
      results.append((validX[i],Z,validY[i],Z==validY[i]))
      if Z==validY[i]:
          success = success + 1
      else:
          failure = failure + 1

  return (float(success)/(success+failure), results)
  

if __name__ == "__main__":
  libraries = [ l[0] for l in csv.reader(open("library_list.csv", "r"))] 
  books = bks.Books() 

  # run classifier
  for l in libraries: 
    loans = (books.libraryLoans(l)).values()
    limit = int(round(0.8*len(loans)))
    train = loans[:limit]
    test = loans[limit+1:]
    # 10 fold validation
    for fold in range(10):
      trainX, trainY, validX, validY, threshold = splitData(train, fold)
      from sklearn.svm import SVC
      clfType = "SVM"
      classifier = SVC()
      
      success_rate, results = runClassifier(
          classifier,
          trainX = trainX, 
          trainY = trainY, 
          validX = validX, 
          validY = validY) 
          
      print "Library " + str(l) + " fold " + str(fold) + " with threshold " + str(threshold) + " success rate is " + str(success_rate)
      with open(clfType+' results/'+'results '+l[:9] + "_fold_" + str(fold)  + '.csv','w') as csvfile:
        writer = csv.writer(csvfile,delimiter = ',', quotechar='\"', quoting=csv.QUOTE_ALL)
        for r in results:
          writer.writerow(r)
