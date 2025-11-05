from app.agent.reasoning_agent import AGENT
from app.utils.helper_functions import *

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def start():
    return f"Listening on port 8080"

@app.route("/ask_gemini", methods=['POST', 'OPTIONS'])
def ask_gemini():
    """Calls a Reasoning Agent to generate a response from the query"""

    if request.method == 'OPTIONS':
        return response_object(" ")
    
    session_id = request.form.get('session_id')
    text = request.form.get('text')
    attachments = request.form.get('attachments')

    query = construct_query(text, [attachments])
    configuration = construct_configuration(session_id)
    
    agent = AGENT()
    model_response = agent.query(query, configuration)
    formatted_output = format_response(model_response)
    
    response = response_object(formatted_output)
    return response