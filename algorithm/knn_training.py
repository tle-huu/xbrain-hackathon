import sys
import pickle
import pandas as pd
import time
from sklearn.neighbors import NearestNeighbors
import numpy as np

from sklearn.externals import joblib


from utils import sentence2vec

##################### Loading the vectorized answers ##########################
def loader(fileName):

	# file_Name = "dictionnaries/answers_dict"
	fileObject = open(fileName,'rb')
	answers = pickle.load(fileObject)

	fileObject.close()
	return answers
###############################################################################

#####################  Traning K NN on Answers ################################

def train_knn(k, dat, filename):
	if k <= 0:
		print("WARNING: number of neighbors should be positive")
		return None
	if k > 3:
		print("k should be 1 or 3")
	print("Start training")
	neigh = NearestNeighbors(n_neighbors=k)
	neigh.fit(dat)
	print("Finished training")

	# Save to file in the current working directory
	# joblib_file = "joblib_model.pkl"
	joblib.dump(neigh, filename)

    #
	# # Pickling model
	# fileObject = open(filename,'wb')
	# pickle.dump(neigh, fileObject)
	# fileObject.close()
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

def main():
	if len(sys.argv) < 3:
		print("Usage: python3 knn_training.py [answers, question] [model file name]")
		return 1
	if sys.argv[1] == "answers":
		data = load("dictionnaries/answers_dict")
	if sys.argv[1] == "questions":
		data = load("dictionnaries/questions_dict")

	train_knn(3, data, argv[2])


	return 1
if __name__ == "__main__":
	main()




	# # Save to file in the current working directory
	# joblib_file = "joblib_model.pkl"
	# # Load from file
	# joblib_model = joblib.load(joblib_file)
    #
	# closest_question = predict("How automatically to forward bitcoins from one address to another", joblib_model)
    #
	# print("Loading csv")
	# data = pd.read_csv("../data/answershtml.csv")
    #
	# print("The closest questions are : ")
	# print(data.text[closest_question[0][0]])
	# print(data.text[closest_question[0][1]])
	# print(data.text[closest_question[0][2]])
