import os
import vertexai
from vertexai.preview import reasoning_engines
import json

from flask import Flask, request, make_response
from google.cloud import discoveryengine
from dotenv import load_dotenv
from google.cloud import discoveryengine_v1 as discoveryengine
from google.api_core.client_options import ClientOptions

     
app = Flask(__name__)

load_dotenv()

PROJECT_ID = os.getenv('PROJECT_ID')
LOCATION = os.getenv('LOCATION_ID')
DATA_STORE_ID = os.getenv('DATA_STORE_ID')
NB_R_ENGINE_ID = os.getenv('NB_R_ENGINE_ID')
NB_R_ENGINE_LOCATION = os.getenv('NB_R_ENGINE_LOCATION')
STAGING_BUCKET = os.getenv('STAGING_BUCKET')
APP_ID = os.getenv('APP_ID')

vertexai.init(project=PROJECT_ID, location=NB_R_ENGINE_LOCATION, staging_bucket=STAGING_BUCKET)

def vertex_search(search_query: str):
    client = discoveryengine.SearchServiceClient()
    
    serving_config = client.serving_config_path(
        project=PROJECT_ID,
        location=LOCATION,
        data_store=DATA_STORE_ID,
        serving_config=APP_ID
    )

    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=search_query,
        page_size=10,
        )
    
    response = client.search(request)

    return response

def get_query(request_object):
    text = request_object.get('text', type=str)
    attachments = request_object.get('attachments')

    query = text + " " + "".join(attachments)
    return query

@app.route("/")
def start():
    return "Listening on port 8080"

@app.route("/search_database", methods=['GET'])
def search_database():

    responses = vertex_search(str(request))
    result = [str(response.document) for response in responses]
    return result
    
remote_agent = reasoning_engines.ReasoningEngine(reasoning_engine_name=NB_R_ENGINE_ID)

@app.route("/ask_gemini", methods=['GET'])
def ask_gemini():
    
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin",'*')
        return response
    else:
        query = request.args.get('query')
        model_output = remote_agent.query(input=query)

        response = make_response(model_output)
        response.headers.add("Access-Control-Allow-Origin",'*')
        return json.dumps(response)
