import flask
import json
import os
from flask import send_from_directory, request

# Flask app should start in global layout
app = flask.Flask(__name__)

@app.route('/')

@app.route('/home')
def home():
    return "Hello World"

@app.route('/webhook', methods=['GET','POST'])
def webhook():

    req = request.get_json(force=True)

    query_text = req.get('sessionInfo').get('parameters').get('query_text')

    answer = "ChatGPT: " + query_text

    res1 = {
        "fulfillment_response": {"messages": [{"text": {"text": [answer]}}]}
    }
    print(type(res1))
    res = {
        "fulfillment_response": {"messages": [{"text": {"text": [answer]}}]}
    }

    return res

if __name__ == "__main__":

    app.run()
    app.debug = True