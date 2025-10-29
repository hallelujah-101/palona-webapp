import os
from dotenv import load_dotenv

import vertexai
from vertexai.preview import reasoning_engines

class AGENT:

    def __init__(self):
        load_dotenv()

        PROJECT_ID = os.getenv('PROJECT_ID')
        LOCATION = os.getenv('LOCATION')
        STAGING_BUCKET = os.getenv('STAGING_BUCKET')
        AGENT_ENGINE_RESOURCE_NAME = os.getenv('AGENT_ENGINE_RESOURCE_NAME')

        vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

        self.remote_agent = reasoning_engines.ReasoningEngine(AGENT_ENGINE_RESOURCE_NAME)

    def query(self, query, configuration):
        return self.remote_agent.query(input=query, config=configuration)
