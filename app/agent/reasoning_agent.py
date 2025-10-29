import os
from dotenv import load_dotenv

import vertexai
from vertexai import agent_engines

class AGENT:

    def __init__(self):
        load_dotenv()

        PROJECT_ID = os.getenv('PROJECT_ID')
        LOCATION = os.getenv('LOCATION')
        STAGING_BUCKET = os.getenv('STAGING_BUCKET')
        AGENT_ENGINE_RESOURCE_NAME = os.getenv('AGENT_ENGINE_RESOURCE_NAME')

        vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

        self.remote_agent = agent_engines.get(AGENT_ENGINE_RESOURCE_NAME)
