import os
import requests
import vertexai

from flask import Flask
from google.cloud import discoveryengine
from dotenv import load_dotenv
     
app = Flask(__name__)

load_dotenv()

PROJECT_ID = os.getenv('PROJECT_ID')
LOCATION = os.getenv('LOCATION_ID')
NB_R_ENGINE_ID = os.getenv('NB_R_ENGINE_ID')
NB_R_ENGINE_LOCATION = os.getenv('NB_R_ENGINE_LOCATION')
STAGING_BUCKET = os.getenv('STAGING_BUCKET')

MAX_RETRIES = 10

@app.route("/")
def start():
    return "Listening on port 8080"

@app.route("/search_db/<query>")
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
    

vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)
client = vertexai.Client(
    project=PROJECT_ID,
    location=LOCATION
)

remote_agent = client.agent_engines.get(name="projects/{PROJECT_ID}/locations/{NB_R_ENGINE_LOCATION}/reasoningEngines/{NB_R_ENGINE_ID}")

@app.route("/ask_gemini/<query>")
def ask_gemini(query):
    response = remote_agent.query(input=query)
    return response['output']