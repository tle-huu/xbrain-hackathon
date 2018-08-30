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

import utils.py

##################### Loading the vectorized answers ##########################
file_Name = "answers_vec_test1"
fileObject = open(file_Name,'rb')
answers = pickle.load(fileObject)
fileObject.close()
###############################################################################

#####################  Traning K NN on Answers ################################

def train_knn(k):
	if k <= 0:
		print("WARNING: number of neighbors should be positive")
		return None
	if k > 3:
		print("k should be 1 or 3")
	neigh = NearestNeighbors(n_neighbors=k)
	neigh.fit(answers)

	# Pickling model
	knnfile = "knn_model"
	fileObject2 = open("answers_dict",'wb')
	pickle.dump(neigh, fileObject2)
	fileObject.close()
###############################################################################

def predict(user_question, neigh):
	try:
		user_question = str(user_question)
	except Exception as e:
		print(str(e))
		return None
	vectest = sentence2vec(user_question)
	res = neigh.kneighbors([vectest], return_distance=False)
	return res		# Return the list of the k nearest neighbors
	# return dico[res[0][0]]		# Return the id of the sentence # Dico.key = vector id
