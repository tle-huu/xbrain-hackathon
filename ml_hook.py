from __future__ import print_function
import pickle
import pandas as pd
from scipy import spatial
import time
from sklearn.externals import joblib

## LOADING DICTIONNARY
file_Name = "en_model"
fileObject = open(file_Name,'rb')
en_model = pickle.load(fileObject)
fileObject.close()

### LOADING KNN MODELS
fileObject = open("models/knn_questions3",'rb')
questionsmodel = pickle.load(fileObject)
fileObject.close()
answersmodel = joblib.load("models/knn_answers3.pkl")

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


def predict(vect_quest, model):
	neighbors = model.kneighbors([vect_quest], return_distance=False)
	return neighbors		# Return the list of the k nearest neighbors

def ret_dict_update(ret_dict, data, i):
    ret_dict['electedAnswer'] = data.text[i + 1]
    ret_dict['bestAnswers'][2] = ret_dict['bestAnswers'][1]
    ret_dict['bestAnswers'][1] = ret_dict['bestAnswers'][0]
    ret_dict['bestAnswers'][0] = data.id[i + 1]
    ret_dict['buckets'][2] = ret_dict['buckets'][1]
    ret_dict['buckets'][1] = ret_dict['buckets'][0]
    ret_dict['buckets'][0] = data.id[i + 1]

    return ret_dict


def ml_hook(question):

    userVect = sentence2vec(question)

    res = 0
    data = pd.read_csv("../data/answershtml.csv")



	bestAnswers = predict(userVect, answersmodel)
	bestQuestions = predict(userVect, questions)


	bestAnswersArray = [0] * 3
	bestAnswersArray[0] = bestAnswers[0][0]
	bestAnswersArray[1] = bestAnswers[0][1]
	bestAnswersArray[2] = bestAnswers[0][2]

	bestQuestionsArray = [0] * 3
	bestQuestionsArray[0] = bestQuestions[0][0]
	bestQuestionsArray[1] = bestQuestions[0][1]
	bestQuestionsArray[2] = bestQuestions[0][2]

	ret_dict = dict()
	ret_dict['buckets'] = bestQuestionsArray
	ret_dict['bestAnswers'] = bestAnswersArray
	ret_dict['electedAnswer'] =  prepare_slack(data.text[bestAnswers[0][0]])

    return ret_dict
