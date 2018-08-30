from flask import Flask, request, jsonify, abort
from ml_hook import ml_hook
import json
import pickle
import pandas as pd
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

file_Name = "answers_vec_test1"
fileObject = open(file_Name,'rb')
answers = pickle.load(fileObject)
fileObject.close()
data = pd.read_csv("../data/answers2.csv")

@app.route("/process", methods=['POST'])
def ask():
    print (request)
    question = ''
    if 'text' in request.form:
        question = request.form['text']
    elif request.json and 'question' in request.json:
        question = request.json['question']
    elif request.json and 'challenge' in request.json:
        print("We have been challenged")
        return request.json['challenge']
    else:
        abort(400)

    print(question)
    # Entry Point For Quesiton to NLP
    ret = ml_hook(question, answers, data)
    print("finished processing")
    # ret = find_answers(question)
    # ret = {
    #     'electedAnswer': "Cause he dislikes Tom Brady",
    #     'buckets': [32, 56, 12],
    #     'bestAnswers': [453, 543, 687]
    # }

    # Printing HTTP Return Body
    print(ret)
    return json.dumps(ret), 200

if __name__ == "__main__":
    app.run()
