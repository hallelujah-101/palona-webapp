import os
from dotenv import load_dotenv

from flask import Flask
from google.cloud import discoveryengine
     
app = Flask(__name__)

load_dotenv()

@app.route("/")
def start():
    return "Listening on port 8080"

@app.route("/searchdb/<query>")
def search_db(query):
    
    client = discoveryengine.SearchServiceClient()
    
    service_config = client.serving_config_path(
        project=os.getenv('PROJECT_ID'),
        location=os.getenv('LOCATION_ID'),
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

