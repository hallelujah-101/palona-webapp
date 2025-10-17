import os
import vertexai
from vertexai.preview import reasoning_engines
import json
from typing import List, Optional
import base64

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

def vertex_search(search_query: str, images: Optional[List[str]]):
    
    client = discoveryengine.SearchServiceClient()
    
    serving_config = client.serving_config_path(
        project=PROJECT_ID,
        location=LOCATION,
        data_store=DATA_STORE_ID,
        serving_config=APP_ID
    )
    
    responses = []
    if images[0] != None: 
        
        for image in images:
            image_query = discoveryengine.SearchRequest.ImageQuery(image_bytes=image)
            request = discoveryengine.SearchRequest(
                serving_config=serving_config,
                query=search_query,
                image_query=image_query,
                page_size=1,
                )
                
            response = client.search(request)
            responses.append(response)
    
    else:

        request = discoveryengine.SearchRequest(
                serving_config=serving_config,
                query=search_query,
                page_size=1,
                )

        response = client.search(request)
        responses.append(response)

    return responses

@app.route("/")
def start():
    return "Listening on port 8080"

@app.route("/search_database", methods=['POST'])
def search_database():

    text = request.form.get('text')
    attachments = request.form.get('attachments')
    
    response_list = vertex_search(text, attachments)
    result = [[str(single_response.document) for single_response in response] for response in response_list]
    return result
    
remote_agent = reasoning_engines.ReasoningEngine(reasoning_engine_name=NB_R_ENGINE_ID)

@app.route("/ask_gemini", methods=['POST', 'OPTIONS'])
def ask_gemini():
        
    text = request.form.get('text')
    attachments = request.form.get('attachments')
    
    query = {'text': text, 'attachments': attachments}
    query_string = json.dumps(query)
    model_output = remote_agent.query(input=query_string)
    
    response = make_response(model_output)
    response.headers.add("Access-Control-Allow-Origin","*")
    response.headers.add("Accept", "*/*")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,PATCH,POST,DELETE")
    response.headers.add("Access-Control-Allow-Headers", "Access-Control-Allow-Origin, Origin, X-Requested-With, Content-Type, Accept")
    return response
