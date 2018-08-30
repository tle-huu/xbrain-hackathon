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

# result = 1 - spatial.distance.cosine(dataSetI, dataSetII)

# Turn a sentence to a vector
def sentence2vec(sentence):
	if sentence == None:
		return None
	split = sentence.split(" ")
	length = len(split)
	vector = [0] * 300
	for word in split:
		if word in en_model.vocab:
			for i in range(300):
				vector[i] += en_model[word][i]
		else:
			length -= 1
	if not length:
		return None
	for i in range(300):
		vector[i] /= length
	return (vector)

# Load the english dictionnary of words-vectors
file_Name = "en_model"
fileObject = open(file_Name,'rb')
en_model = pickle.load(fileObject)
fileObject.close()

data = pd.read_csv("../data/answers2.csv")

doc = []

dico = {}

print("Beginning")
for i in range(len(data)):
	vec = sentence2vec(data.text[i])
	id_ = data.id[i]
	if vec != None:
		doc.append(vec)
		dico[tuple(vec)] = id_

print("Vectorized")
fileObject = open("answers_dict",'wb')
pickle.dump(dico, fileObject)
fileObject.close()

true_k = 5
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
print("Training")
model.fit(doc)
print("End Training...")
fileObject2 = open("modelkmeans", 'wb')
pickle.dump(model, fileObject2)
fileObject2.close()

colors = ['r', 'b', 'g', 'y', 'c', 'm']
svd = TruncatedSVD(n_components=2).fit(doc)
centers2D = svd.transform(model.cluster_centers_)
doc2D = svd.transform(doc)

for i in range(len(model.cluster_centers_)):
	plt.scatter(centers2D[i,0], centers2D[i,1],
	            marker='x', s=200, linewidths=3, c=colors[i])

for i in range(len(doc)):
	plt.scatter(doc2D[i,0], doc2D[i,1], c=colors[model.labels_[i]])
plt.hold(True)

plt.show()
