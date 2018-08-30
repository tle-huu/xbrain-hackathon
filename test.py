from flask import Flask, request, jsonify, abort

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


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
    # ret = find_answers(question)
    ret = {
        'electedAnswer': "Cause he dislikes Tom Brady",
        'buckets': [32, 56, 12],
        'bestAnswers': [453, 543, 687]
    }

    # Printing HTTP Return Body
    print()
    print("raw ret : ", end='')
    print(ret)
    print("json : ", end='')
    print(jsonify(ret))
    print("---")
    print()
    return jsonify(ret), 200

if __name__ == "__main__":
    app.run()
