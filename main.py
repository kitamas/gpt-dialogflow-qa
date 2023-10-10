import flask
import json
import os
from flask import send_from_directory, request
import openai
import pinecone

# Heroku config vars
# openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_key = "sk- . . ."

# Heroku config vars
PINECONE_API_KEY = os.getenv.get("PINECONE_API_KEY")
# TELEKOM PINECONE_API_KEY = "c47d17e1-62da-4f4a-a319-9608e3104d13"
# PINECONE_API_KEY = "a2a86279-ffc8-490c-9365-0d3d32a458a5"

# TELEKOM YOUR_ENV = "us-west1-gcp-free"
YOUR_ENV = "us-west4-gcp"

index_name = "chat-doc-mt"

namespace = "Moodle_QA"

# Flask app should start in global layout
app = flask.Flask(__name__)

@app.route('/')

@app.route('/home')
def home():
    return "Hello World"

# def complete_xq(query):
def complete_xq(query,namespace):
    # openai.api_key = "sk- . . ."

    # initializing a Pinecone index
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=YOUR_ENV
    )

    index = pinecone.Index(index_name)

    xq = openai.Embedding.create(input=query, engine=MODEL)['data'][0]['embedding']

    res = index.query([xq], top_k=1, include_metadata=True, namespace=namespace)
   
    """
    print("\nThe most similar questions:")
    for match in res['matches']:
        print(f"{match['score']:.2f}: {match['metadata']['question']}")
    """
          
    # print("\nAnswer:")    
    for match in res['matches']:
        # print(f"{match['score']:.2f}: {match['metadata']['answer']}\n")
        # print(f"\nURL: {match['metadata']['url']}\n\nTITLE: {match['metadata']['title']}\n\nSPAN: {match['metadata']['span']}\n\nDIV: {match['metadata']['div']}\n")

        query = f"{match['metadata']['answer']}"
        # query = f"\nURL: {match['metadata']['url']}\n\nTITLE: {match['metadata']['title']}\n\nSPAN: {match['metadata']['span']}\n\nDIV: {match['metadata']['div']}\n"
        return query

    #return query


@app.route('/webhook', methods=['GET','POST'])
def webhook():

    # openai.api_key = "sk- . . ."

    # initializing a Pinecone index
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=YOUR_ENV
    )

    index = pinecone.Index(index_name)

    req = request.get_json(force=True)

    query_text = req.get('sessionInfo').get('parameters').get('query_text')
    namespace = req.get('sessionInfo').get('parameters').get('namespace')
    # print("namespace = ",namespace)
    # query_with_contexts = retrieve(query_text)

    # answer = complete_xq(query_with_contexts)
    # answer = complete_xq(query_text)
    # answer = "ChatGPT: " + complete_xq(query_text)
    # answer = "ChatGPT: " + complete_xq(query_text,namespace)
    answer = "ChatGPT: "

    res = {
        "fulfillment_response": {"messages": [{"text": {"text": [answer]}}]}
    }

    return res

embed_model = "text-embedding-ada-002"
MODEL = "text-embedding-ada-002"
# namespace = namespace

"""
def retrieve(query_text):
    ...

    return prompt
"""

if __name__ == "__main__":

    app.run()
#    app.debug = True