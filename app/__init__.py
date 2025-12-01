import logging
from typing import List
from app.agent.reasoning_agent import AGENT
from app.utils.helper_functions import *
from flask import Flask, request


app = Flask(__name__)
agent = AGENT()

@app.route("/")
def start():
    return f"Listening ....."

@app.route("/ask_gemini", methods=['POST', 'OPTIONS'])
async def ask_gemini():
    """Query a reasoning Agent to generate a response from the query"""
    
    empty_response = response_object(" ")
    if request.method == 'OPTIONS':
        return empty_response
        
    session_id: str = request.form.get('session_id')
    text: str = request.form.get('text')
    attachments: List[str] = request.form.getlist('attachments')
    
    model_response = await agent.query(text, attachments, session_id)
    
    response = None
    if model_response:
        response = response_object(model_response)
    else:
        response = empty_response
        
    return response