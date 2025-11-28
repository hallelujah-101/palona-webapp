import re
from flask import make_response

def construct_configuration(session_id):
    return {"configurable": {"session_id": f"{session_id}"}}

def construct_query(text, images):
    return f"input: {text}, images: {images}"
    
def response_object(content):
    
    response = make_response(content)
    response.headers.add("Access-Control-Allow-Origin","*")
    response.headers.add("Accept", "*/*")
    response.headers.add("Access-Control-Allow-Methods", "OPTIONS, POST")
    response.headers.add("Access-Control-Allow-Headers", "Access-Control-Allow-Origin, Origin, X-Requested-With, Content-Type, Accept")

    return response