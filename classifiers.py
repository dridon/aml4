from sklearn import neighbors
import books as bks
import csv
import numpy as np

numFolds = 4

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
        norm.append([d[0]/1000.0,d[1]/maxPos,d[2]/maxNeg,d[3]/2014.0])
    return norm

def avg(data):
    return sum(data)/float(len(data))    
    
def splitData(loans, fold):
  trainSet = []
  validSet =[]
  i = 0
  
  for book in loans:
      i = i + 1
      if i%numFolds != fold:
          trainSet.append(book)
      else:
          validSet.append(book)
  threshold = calcThreshold(trainSet,"median")
  authDict,maxPos,maxNeg = circInfo(trainSet, threshold)

  trainX = []
  trainY = []
  validX = []
  validY = []
  for book in trainSet:
      if book.author[0] == '':
          circ = [0,0]
      else:
          circ = authDict[book.author]
      trainX.append([book.callno,book.year])
      #trainX.append([book.callno,circ[0],circ[1],book.year])
      if book.circ > threshold:
          trainY.append(1)
      else:
          trainY.append(0)
          
  for book in validSet:
      if book.author in authDict:
          circ = authDict[book.author]
      else:
          circ = [0,0]
      validX.append([book.callno,book.year])
      #validX.append([book.callno,circ[0],circ[1],book.year])
      if book.circ > threshold:
          validY.append(1)
      else:
          validY.append(0)

  return (trainX, trainY, validX, validY, threshold)

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
      results.append((validX[i],Z,validY[i],Z==validY[i]))
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
  
  libraries = ["Plateau-Mont-Royal","Rosemont - La Petite-Patrie","Saint-Laurent","Anjou","Mercier-Hochelaga-Maisonneuve"]
  books = bks.Books() 

  # run classifier
  for neighbours in range(10,60,10):
      classifier = neighbors.KNeighborsClassifier(neighbours)
      for l in libraries: 
          loans = (books.libraryLoans(l)).values()
          limit = int(round(0.8*len(loans)))
          train = loans[:limit]
          test = loans[limit+1:]
    
          success=[]
          sens = []
          spec = []
        # 10 fold validation
          for fold in range(numFolds):
              trainX, trainY, validX, validY, threshold = splitData(train, fold)
              success_rate, sensitivity,specificity,results = runClassifier(
                  classifier,
                  trainX = trainX, 
                  trainY = trainY, 
                  validX = validX, 
                  validY = validY) 
              success.append(success_rate)
              sens.append(sensitivity)
              spec.append(specificity)
              with open('results/'+'results '+l[:9] + "_fold_" + str(fold)  + '.csv','w') as csvfile:
                  writer = csv.writer(csvfile,delimiter = ',', quotechar='\"', quoting=csv.QUOTE_ALL)
                  for r in results:
                      writer.writerow(r)
          print neighbours, l, avg(success),avg(sens),avg(spec)
          