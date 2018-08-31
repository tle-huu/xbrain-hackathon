from __future__ import print_function
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

    file_Name = "answers_vec_test1"

    fileObject = open(file_Name,'rb')

    answers = pickle.load(fileObject)
    fileObject.close()

    vectest = sentence2vec(question)
    res = 0
    data = pd.read_csv("../data/answers3.csv")



    ret_dict = dict()
    ret_dict['bestAnswers'] = [None, None, None]
    ret_dict['buckets'] = [None, None, None]

    t = time.clock()
    for i in range(len(answers)):
        shutup = spatial.distance.euclidean(vectest, answers[i])
        if shutup < similarity:
            ret_dict = ret_dict_update(ret_dict, data, i)
            print(i)
            print(data.text[i])
            print()
            similarity = shutup
            res = i
    print("time : {}".format(time.clock() - t))
    print("Res {}".format(res))
    print("The most similar answers for {} is {}\n".format(question, data.id[res]))

    print(data.text[res])
    return ret_dict
