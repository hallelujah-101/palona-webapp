import os
import requests
from dotenv import load_dotenv

from flask import Flask
from google.cloud import discoveryengine
from vertexai.preview import reasoning_engines

     
app = Flask(__name__)

load_dotenv()

PROJECT_ID = os.getenv('PROJECT_ID')
LOCATION = os.getenv('LOCATION_ID')
NB_R_ENGINE_ID = os.getenv('NB_R_ENGINE_ID')
MAX_RETRIES = 10

@app.route("/")
def start():
    return "Listening on port 8080"

@app.route("/searchdb/<query>")
def search_db(query):
    
    client = discoveryengine.SearchServiceClient()
    
    service_config = client.serving_config_path(
        project=PROJECT_ID,
        location=LOCATION,
        data_store=os.getenv('DATA_STORE_ID'),
        serving_config=os.getenv('APP_ID')
    )

    request = discoveryengine.SearchRequest(
        serving_config=service_config,
        query=query,
        page_size=1
    )
    
    responses = client.search(request)
    result = [str(response.document) for response in responses]
    return result

remote_agent = reasoning_engines.ReasoningEngine(
    f"projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{NB_R_ENGINE_ID}"
)
@app.route("/ask_gemini/<query>")
def ask_gemini(query):
    retries = 0
    resp = None
    while retries < MAX_RETRIES:
        try:
            retries += 1
            resp = remote_agent.query(input=query)
            if (resp == None) or (len(resp["output"].strip()) == 0):
                raise ValueError("Empty response.")
            break
        except Exception:
            if (resp == None) or (len(resp["output"].strip()) == 0):
                raise ValueError("Too many retries.")
                return "No response received from Reasoning Engine."
            else:
                return resp["output"]
