import ctypes as ct 
import numpy as np


class Word2Vec:
  vectors_file = None
  vectors_lib = None
  vectors = None
  word_vectors = None
  vocab = {} 
  c_vec = None

  def __init__(self, vectors_file):
    """
      Loads the word vocabulary and vectors from a bin file. 
    """
    self.vectors_file = vectors_file
    self.vectors_lib = ct.cdll.LoadLibrary("./word2vec.so")

    # set the return types of the library functions 
    self.vectors_lib.get_vocab.restype = ct.POINTER(ct.c_char_p)
    self.vectors_lib.word_count.restype = ct.c_longlong
    self.vectors_lib.vector_size.restype = ct.c_longlong
    self.vectors_lib.get_vector.restype = ct.POINTER(ct.c_float)

    # load the vectors
    self.vectors_lib.initialize(vectors_file)

    # create a dictionry index of words for fast look up
    self.__load_vocab_index__()

  def __load_vocab_index__(self): 
    """
      Creates a vocabulary index for fast vector lookup
    """
    print "creating index dictionary" 
    vocab = self.vectors_lib.get_vocab()
    word_count = self.vectors_lib.word_count()

    for i in range(word_count):
      self.vocab[vocab[i]] = i 
    print "dictionary completed"

  def get_vector(self, word): 
    """
      Returns the vector as a numpy array for the given word and None if it does not exist 
      in the library
    """
    if word not in self.vocab: 
      print "Warning: word " + word + " does not exist in vocabulary!"
      return None 

    vec = self.vectors_lib.get_vector(self.vocab[word])
    v = np.zeros(self.vectors_lib.vector_size())
    for i in range(self.vectors_lib.vector_size()): 
      v[i] = vec[i]
    return v

if __name__ == "__main__": 
  wv = Word2Vec("GoogleNews-vectors-negative300.bin")
  print wv.get_vector("Paul")
