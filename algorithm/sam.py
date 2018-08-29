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


file_Name = "en_model"
fileObject = open(file_Name,'rb')
en_model = pickle.load(fileObject)
fileObject.close()

def sentence2vec(sentence):
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
		print(split)
		return None
	for i in range(300):
		vector[i] /= length
	return (vector)


file_Name = "answers_vec_test1"

fileObject = open(file_Name,'rb')

answers = pickle.load(fileObject)
fileObject.close()

test_question = "no access to usb port when running python script on boot"
vectest = sentence2vec(test_question)

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
