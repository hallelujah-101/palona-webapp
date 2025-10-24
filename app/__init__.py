import os
import vertexai
from vertexai.preview import reasoning_engines
from typing import List, Optional
import re
import pickle

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
    """Connect to the Vertex Search resource and fetches search results based on the query."""
    
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
            response_documents = get_top_documents(response)
            responses.append(response_documents)

    else:
        
        request = discoveryengine.SearchRequest(
                serving_config=serving_config,
                query=search_query,
                page_size=1,
                )
        
        response = client.search(request)
        response_documents = get_byte_form(response)
        responses.append([response_documents])
    
    return responses

@app.route("/")
def start():
    return f"Listening on port 8080"


@app.route("/search_database", methods=['POST'])
def search_database():
    """Calls the function that initiates the search"""
    
    text = request.form.get('text')
    attachments = request.form.get('attachments')
    
    response_list = vertex_search(text, attachments)
    return response_list

def get_top_documents(response, count = 100):
    """Get the top 'count' documents from a search result"""

    documents = []
    for result in response:
        if count > 0:
            documents.append(str(result.document))
            count -=1
        else:
            break

    return documents

def get_byte_form(response):

    results = []
    for result in response:
        results.append(pickle.dumps(result.document))

    return results

def search_database(text, attachments):
    
    response_list = vertex_search(text, attachments)
    return response_list

remote_agent = reasoning_engines.ReasoningEngine(reasoning_engine_name=NB_R_ENGINE_ID)

@app.route("/ask_gemini", methods=['POST', 'OPTIONS'])
def ask_gemini():
    """Calls a Vertex AI Search resource and passes the data to a Reasoning Agent to generate a response"""
    
    session_id = request.form.get('session_id')
    text = request.form.get('text')
    attachments = request.form.get('attachments')
    
    database_output = search_database(text,[attachments])
    
    query = f'input: {text} database_output: {database_output}'
    model_response = remote_agent.query(input=query, config={"configurable": {"session_id": f"{session_id}"}})
    model_output = model_response['output']
    
    response_type = 0
    formatted_output = ''
    if 'json' in model_output:
        output = model_output.split('json')[1]
        formatted_output = re.sub(r'[\n`]', '', output)
        response_type = 1
    else:
        formatted_output = model_output
    
    response = make_response(formatted_output)
    response.headers.add("Agent-Response",f"{response_type}")
    response.headers.add("Access-Control-Allow-Origin","*")
    response.headers.add("Accept", "*/*")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,PATCH,POST,DELETE")
    response.headers.add("Access-Control-Allow-Headers", "Access-Control-Allow-Origin, Origin, X-Requested-With, Content-Type, Accept")
    return response
