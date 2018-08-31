from __future__ import print_function
from gensim.models import KeyedVectors
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import Pipeline
import pickle
import pandas as pd
from scipy import spatial
from utils import sentence2vec

# result = 1 - spatial.distance.cosine(dataSetI, dataSetII)

# Load the Stack Over Flow dictionnary of words-vectors
print("Loading vocab")
file_Name = "en_model"
fileObject = open(file_Name,'rb')
en_model = pickle.load(fileObject)
fileObject.close()

print("Loading csv")
data = pd.read_csv("../data/answers2.csv")

dico = []

print("Beginning")
for i in range(len(data)):
	vec = sentence2vec(data.text[i])
	if vec != None:
		dico.append(vec)
		# dico[i] = vec
	else:
		nul = [0] * 300
		dico.append(nul)
print("Vectorized")
fileObject = open("answers_dict",'wb')
pickle.dump(dico, fileObject)
fileObject.close()
