import os
from dotenv import load_dotenv

from google.adk.agents import Agent
import vertexai
from vertexai import agent_engines

class AGENT:

    def __init__(self):
        """Initialises the vertex ai project and reasoning engine"""
        load_dotenv()

        PROJECT_ID = os.getenv('PROJECT_ID')
        LOCATION = os.getenv('LOCATION')
        STAGING_BUCKET = os.getenv('STAGING_BUCKET')
        AGENT_ENGINE_RESOURCE_NAME = os.getenv('AGENT_ENGINE_RESOURCE_NAME')
        
        vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)
        
        agents_list = list(vertexai.agent_engines.list())
        if agents_list:
            self.remote_agent = agents_list[0]  
            client = agent_engines
            print(f"✅ Connected to deployed agent: {self.remote_agent.resource_name}")
        else:
            print("❌ No agents found. Please deploy first.")

    async def query(self, query, user_id): 
        
        async for event in self.remote_agent.async_stream_query(
            message=query,
            user_id=user_id,
        ):
            
            if 'content' in event.keys() and ('parts' in event['content'].keys()):
                for part in event['content']['parts']:
                    if 'function_response' in part.keys():
                        if part['function_response']['name'] == 'output_formatter':
                            return part['function_response']['response']
        
        return None