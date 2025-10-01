from flask import Flask , render_template
from google.cloud import discoveryengine
     
app = Flask(__name__)

PROJECT_ID = "mindful-phalanx-473719-j7"
DATA_STORE_ID = "palona-fasion-data_1759263624316"
LOCATION_ID = "global"
APP_ID = "letshop_1759263815422"


@app.route("/")
def start():
    return "Listening on port 8000"

@app.route("/searchdb/<query>")
def search_db(query):
    
    client = discoveryengine.SearchServiceClient()
    
    service_config = client.serving_config_path(
        project=PROJECT_ID,
        location=LOCATION_ID,
        data_store=DATA_STORE_ID,
        serving_config=APP_ID
    )

    request = discoveryengine.SearchRequest(
        serving_config=service_config,
        query=query,
        page_size=1
    )
    
    responses = client.search(request)
    result = [str(response.document.content) for response in responses]
    return result

if __name__ == '__main__':
    app.run(port=8000)