from flask import Flask, request, jsonify, abort, json
from ml_hook import ml_hook
import requests


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/process", methods=['POST'])
def process():
    channel = None
    response_url = None
    if 'text' in request.form:
        question = request.form['text']
        response_url = request.form['response_url']
    elif request.json and 'question' in request.json:
        question = request.json['question']
    elif request.json and 'challenge' in request.json:
        print("We have been challenged")
        return request.json['challenge']
    elif request.json and 'event' in request.json:
        print(request.json['event'])
        if 'subtype' in request.json['event'] and request.json['event']['subtype'] == 'bot_message':
            return '', 200
        channel = request.json['event']['channel']
        question = request.json['event']['text']
    else:
        abort(400)
        return

    # POST to /ask route. this allows async execution of delayed response processing
    quest_dict = {'question': question,
                  'response_url': response_url,
                  'channel': channel}
    respon = requests.post('http://localhost:5000/ask', json=quest_dict)

    # Response to Slack app. This tells the app we are going to send another response
    # after we process the question
    if response_url is not None or channel is not None:
        respon_dict = {'text': "We are working on finding that result",
                       'response_type': 'in_channel'}
        return jsonify(respon_dict), 200

    ret = app.response_class(
        response=json.dumps(respon.json()),
        status=200,
        mimetype='application/json'
    )
    # print(respon.json)
    return ret


@app.route("/ask", methods=['POST'])
def ask():
    if request.json and 'question' in request.json and 'response_url' in request.json:
        question = request.json['question']
        response_url = request.json['response_url']
        channel = request.json['channel']
    else:
        abort(500)
        return

    # Entry Point For Quesiton to NLP
    print(question)

    ret = ml_hook(question)
    #
    # ret = {
    #         'acceptedAnswer': "Tom Brady",
    #         'buckets': [12, 12, 12],
    #         'bestAnswers': [12, 12, 12]
    #        }

    # Sending to slack URL delayed response
    if response_url is not None:
        data = {'text': ret['electedAnswer'],
                'response_type': 'in_channel'}
        requests.post(response_url, json=data)
    elif channel is not None:
        data = {"ok": True,
                "channel": channel,
                "text": ret['electedAnswer'],
                "type": "message",
                }
        requests.post("https://slack.com/api/chat.postMessage", json=data, headers={'Content-type': 'application/json',
                                                                                     'Authorization': 'Bearer xoxb-422880813170-425052980706-1hJdyfUdOGTAx6RtAS7tJsaI'})

    print()
    print("raw ret : ", end='')
    print(ret)
    print()
    return jsonify(ret), 200

if __name__ == "__main__":
    app.run()
