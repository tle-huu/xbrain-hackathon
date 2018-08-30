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
import time
from sklearn.neighbors import NearestNeighbors


file_Name = "en_model"
fileObject = open(file_Name,'rb')
en_model = pickle.load(fileObject)
fileObject.close()

file_Name = "answers_vec_test1"

fileObject = open(file_Name,'rb')

answers = pickle.load(fileObject)
fileObject.close()

dico = {}
for i in range(len(answers)):
	dico[tuple(answers[i])] = i

test_question = "no access to usb port when running python script on boot"
vectest = sentence2vec(test_question)

neigh = NearestNeighbors(n_neighbors=1)
neigh.fit(answers)

res = neigh.kneighbors([vectest], return_distance=False)

a = dico[tuple(answers[res[0][0]])]

svd = TruncatedSVD(n_components=2).fit(answers)
others = svd.transform(answers)

vectest2 = svd.transform([vectest])

for i in range(len(others)):
	if i == 8:
		plt.scatter(others[i,0], others[i,1], marker='v', c='g')
	else:
		plt.scatter(others[i,0], others[i,1], marker='x', c='b')
plt.scatter(vectest2[:,0], vectest2[:,1], marker='o')
# plt.show()

res = 0
similarity = 7897474684545
data = pd.read_csv("../data/answers2.csv")
print(data.text[a])
sys.exit(1)
t = time.clock()
for i in range(len(answers)):
	shutup = spatial.distance.euclidean(vectest, answers[i])
	if shutup < similarity:
		print(i)
		print(data.text[i])
		print()
		similarity = shutup
		res = i
print("time : {}".format(time.clock() - t))
print("Res {}".format(res))
print("The most similar answers for {} is {}\n".format(test_question, data.id[res]))

print(data.text[res])
