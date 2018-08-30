import pickle

from gensim.models import KeyedVectors

en_model = KeyedVectors.load_word2vec_format('./train.vec')

file_Name = "en_model"
fileObject = open(file_Name,'wb')
pickle.dump(en_model,fileObject)
fileObject.close()
