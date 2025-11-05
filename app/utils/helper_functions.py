import re
from flask import make_response

def construct_configuration(session_id):
    return {"configurable": {"session_id": f"{session_id}"}}

def construct_query(text, images):
    return f"input: {text}, images: {images}"

def format_response(response):

    model_output = response['output']
    
    special_characters_removed = re.sub(r'[\n`]', '', model_output)
    opening_brackets_inserted = special_characters_removed.replace('(', '{')
    closing_brackets_inserted = opening_brackets_inserted.replace(')', '}')
    formatted_output = closing_brackets_inserted.replace('\'', '\"')

    return formatted_output
    

def response_object(content):
    
    response = make_response(content)
    response.headers.add("Access-Control-Allow-Origin","*")
    response.headers.add("Accept", "*/*")
    response.headers.add("Access-Control-Allow-Methods", "OPTIONS, POST")
    response.headers.add("Access-Control-Allow-Headers", "Access-Control-Allow-Origin, Origin, X-Requested-With, Content-Type, Accept")

    return response