import re
from flask import make_response

def construct_configuration(session_id):
    return {"configurable": {"session_id": f"{session_id}"}}

def construct_query(text, images):
    print("Inputs", text, images)
    return f"input: {text}, images: {images}"

def format_response(response):

    model_output = response['output']
    
    if 'json' in model_output:
        output = model_output.split('json')[1]
        formatted_output = re.sub(r'[\n`]', '', output)
        return formatted_output
    else:
        return model_output

def response_object(content):
    
    response = make_response(content)
    response.headers.add("Access-Control-Allow-Origin","*")
    response.headers.add("Accept", "*/*")
    response.headers.add("Access-Control-Allow-Methods", "OPTIONS, POST")
    response.headers.add("Access-Control-Allow-Headers", "Access-Control-Allow-Origin, Origin, X-Requested-With, Content-Type, Accept")

    return response