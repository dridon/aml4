#McGill COMP 598 Final Project: 

##Group Members: 
 * Ali Emami 
 * Faiz Khan 
 * Fernando Sa-Pereira

##Topic: 
Book Recommender System for Montreal Libraries

##Dependencies: 
  * scikit-learn 
  * matplotlib 
  * google word2vec pretrained vectors for google news group (https://code.google.com/p/word2vec/)
  * Encog neural network library
  * gcc
  * make

##Dataset: 
  The raw dataset is available from download at http://donnees.ville.montreal.qc.ca/dataset/catalogue-bibliotheques/resource/67a95c30-4e21-4346-83f7-491d4ca54a7e. The cleaned version is available on the repo in the file nonfiction-no-accents.csv.zip. The extracted file is required for the code to run. 
  
##Modules: 
###Dewey Dictionary 
  This module contains one python file with one class DeweyCode that requires an input file that contains the translations of dewey codes to a unicode equivalent. The file for english provided in dewey\_dictionary.csv. The class can then be used to generate the english counterparts of any of the dewey codes. The key method for this class is dewey\_classes_extract. 

###Word vectors 
  This module governs the wrapper around the google word vectors. word2vec.c contains the code that python wraps around. The makefile produces the required binary and the wordvectors.py provides access to the vectors via python. 

###Books 
  This module makes use of the dewey dictionary and wordvector modules along with the cleaned dataset to generate loan and word vector information on all the books. This module is comosed of books.py and requires stop words for english and french that are provided under eng-stopwords.csv and fr-stopwords.csv. 

###Classifiers
  There are three main components to the classifiers. Classifiers.py contains all the code for our kNN and Naive Bayes runs. The runs for svm are in svm.py. Neural networks were done in Java and are available in the neural_nets folder as an eclipse project. This module requiers the list of libraries to be processed. The libraries used for cross validation are available in library\_list2.csv and all of the libraries used for testing are available in library_list.csv. 
  
##Running the code: 
  To execute the code first clone the repo. Then run the makefile to generate the required word vector binary. Download the google news bin.gz file and uncompress it, its around 3GB in size. The entire file gets loaded to memory so ensure that enough RAM is available otherwise the code becomes very slow. To run kNN or Naive Bayes, go in to classifiers.py and set the required parameters then simply execute the file in the interpreter. The same applies for svm.py. The neural networks require the project to be loaded in Eclipse and compiled. The java code requires some paths to be set, so be vary on that part. The code also requires the input csvs to be generated which can be done with a slight modification of the code in classifiers.py. The code will try to save the results into specific directories so make sure there are directories with the names kNN\_results, NB\_results and SVM\_results in the folder. 
  
####Happy Book Recommending!
  



