import os
import logging
import requests
import vertexai
from vertexai.preview import reasoning_engines

from flask import Flask, request
from google.cloud import discoveryengine
from dotenv import load_dotenv
from google.cloud import discoveryengine_v1 as discoveryengine
from google.api_core.client_options import ClientOptions

     
app = Flask(__name__)

load_dotenv()

PROJECT_ID = os.getenv('PROJECT_ID')
LOCATION = os.getenv('LOCATION_ID')
NB_R_ENGINE_ID = os.getenv('NB_R_ENGINE_ID')
NB_R_ENGINE_LOCATION = os.getenv('NB_R_ENGINE_LOCATION')
STAGING_BUCKET = os.getenv('STAGING_BUCKET')
APP_ID = os.getenv('APP_ID')


vertexai.init(project=PROJECT_ID, location=NB_R_ENGINE_LOCATION, staging_bucket=STAGING_BUCKET)

def search_sample(project_id: str, location: str, engine_id: str, search_query: str):
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    client = discoveryengine.SearchServiceClient(client_options=client_options)

    serving_config = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/servingConfigs/default_config"

    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=search_query,
        page_size=10,
        )
    
    response = client.search(request)

    return response

@app.route("/")
def start():
    return "Listening on port 8080"

@app.route("/search_db", methods=['POST'])
def search_db():
    data = request.json
    query = data.get('query')
    print(query)
    
    responses = search_sample(PROJECT_ID, LOCATION, APP_ID, query)
    result = [str(response.document) for response in responses]
    return result
    
remote_agent = reasoning_engines.ReasoningEngine(reasoning_engine_name=NB_R_ENGINE_ID)

@app.route("/ask_gemini", methods=['POST'])
def ask_gemini():
    prompt_data = request.json
    query = prompt_data.get('query')
    print(query)
    
    response = remote_agent.query(input=query)
    return response['output']
