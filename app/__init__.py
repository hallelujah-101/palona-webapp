import os
import vertexai
import re

from flask import Flask, request, make_response
from dotenv import load_dotenv
from vertexai import agent_engines

app = Flask(__name__)

load_dotenv()

PROJECT_ID = os.getenv('PROJECT_ID')
LOCATION = os.getenv('LOCATION')
STAGING_BUCKET = os.getenv('STAGING_BUCKET')
AGENT_ENGINE_RESOURCE_NAME = os.getenv('AGENT_ENGINE_RESOURCE_NAME')

vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)
remote_agent = agent_engines.get(AGENT_ENGINE_RESOURCE_NAME)

@app.route("/")
def start():
    return f"Listening on port 8080"

@app.route("/ask_gemini", methods=['POST', 'OPTIONS'])
def ask_gemini():
    """Calls a Reasoning Agent to generate a response from the query"""
        
    session_id = request.form.get('session_id')
    text = request.form.get('text')
    attachments = request.form.get('attachments')
    
    query = f"input: {text}, images: {attachments}"
    model_response = remote_agent.query(input=query, config={"configurable": {"session_id": f"{session_id}"}})
    model_output = model_response['output']
    
    output = model_output.split('json')[1]
    formatted_output = re.sub(r'[\n`]', '', output)
    
    response = make_response(formatted_output)
    response.headers.add("Access-Control-Allow-Origin","*")
    response.headers.add("Accept", "*/*")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,PATCH,POST,DELETE")
    response.headers.add("Access-Control-Allow-Headers", "Access-Control-Allow-Origin, Origin, X-Requested-With, Content-Type, Accept")
    return response
