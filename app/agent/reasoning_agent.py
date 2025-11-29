import os
from dotenv import load_dotenv
from typing import Optional, List

import vertexai
from vertexai import agent_engines
from google.cloud import discoveryengine
from google.adk.memory import VertexAiMemoryBankService
from google.adk.sessions import VertexAiSessionService
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from google.adk.agents import Agent
from google.adk.runners import Runner


class AGENT:

    def __init__(self):
        """Initialises the vertex ai project and reasoning engine"""
        
        load_dotenv()
        
        self.PROJECT_ID = os.getenv('PROJECT_ID')
        self.LOCATION = os.getenv('LOCATION')
        self.LOCATION_ID = os.getenv('LOCATION_ID')
        self.STAGING_BUCKET = os.getenv('STAGING_BUCKET')
        self.DATASTORE_ID = os.getenv('DATASTORE_ID')
        self.APP_ID = os.getenv('APP_ID')
        self.AGENT_ENGINE_ID = os.getenv('AGENT_ENGINE_ID')
        self.MODEL = os.getenv('MODEL_NAME')
                
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"
        os.environ["GOOGLE_CLOUD_PROJECT"] = self.PROJECT_ID
        os.environ["GOOGLE_CLOUD_LOCATION"] = self.LOCATION
        
        self.agent_instruction = """ You are a helpful and funny conversational agent named Gemi, and you are a Gemini.
                            1. You provide users with recommendations and search results from a catalogue using the vertex_search tool. 
                            2. You take user questions which may or may not contain images and if they are product related search through a database using the vertex_search tool which allows for text and image search, if they aren't product related you respond with a general response.
                            3. You use the output_formatter tool to, when the response from the vertex_search tool has products, by extracting the ProductTitle, Gender, ProductId and Category fields from the result for each product
                            4. You use the output_formatter tool to form the final response for all queries and just use the text part of the response if the response doesn't contain products
                            You do not give the user details of any intermediate steps and data"""
        
        vertexai.init(project=self.PROJECT_ID, location=self.LOCATION, staging_bucket=self.STAGING_BUCKET)
        
        self.agent = Agent(
                            model=self.MODEL,
                            name="catalogue_query_agent",
                            tools=[PreloadMemoryTool(), self.vertex_search, self.output_formatter],
                            after_agent_callback=self.add_session_to_memory,
                            instruction=self.agent_instruction,
                        )
                        
        self.session_service = VertexAiSessionService(
            project=self.PROJECT_ID, location=self.LOCATION, agent_engine_id=self.AGENT_ENGINE_ID
        )
        
        self.memory_service = VertexAiMemoryBankService(
            project=self.PROJECT_ID, location=self.LOCATION, agent_engine_id=self.AGENT_ENGINE_ID
        )
        
        self.runner = Runner(
            app_name=self.agent.name, 
            agent=self.agent,
            session_service=self.session_service,
            memory_service=self.memory_service,
        )
        
        
        
        
    async def add_session_to_memory(self, callback_context: CallbackContext) -> Optional[types.Content]:
        """Automatically save completed sessions to memory bank """
        if hasattr(callback_context, "_invocation_context"):
            invocation_context = callback_context._invocation_context
            if invocation_context.memory_service:
                await invocation_context.memory_service.add_session_to_memory(
                    invocation_context.session
                )
    
    async def query(self, query, attachments, user_id): 
        session = await self.session_service.create_session(
            app_name=self.agent.name, 
            user_id=user_id,
        )
        content = types.Content(role="user", parts=[types.Part(text=query), types.Part(content=attachments)])
        events = self.runner.run(
            user_id=session.user_id, session_id=session.id, new_message=content
        )

        for event in events:
            if event.is_final_response():
                final_response = event.content.parts[0].text
                return f"Agent Response: {final_response}"
            
            if event.content:
                if event.content.parts[0].function_response:
                    if event.content.parts[0].function_response.name == 'output_formatter':
                        if 'error' in event.content.parts[0].function_response.response.keys():
                            continue
                        else:
                            return event.content.parts[0].function_response.response
                    
    
    def output_formatter(self, text_response: str, product_list: Optional[List]):
        """Format output using the summary response text and list of products in the agent response"""

        return {"response": text_response, "products": product_list}
        
    def vertex_search(self, search_query: str, images: Optional[List[str]] = []):
        """Connect to the Vertex AI Search resource and fetches search results based on the query."""
        from google.cloud import discoveryengine

        client = discoveryengine.SearchServiceClient()

        serving_config = client.serving_config_path(
            project=self.PROJECT_ID,
            location=self.LOCATION_ID,
            data_store=self.DATASTORE_ID,
            serving_config=self.APP_ID
        )

        responses = []
        if len(images) > 0 and (None not in images):

            for image in images:
                image_query = discoveryengine.SearchRequest.ImageQuery(image_bytes=image)
                request = discoveryengine.SearchRequest(
                    serving_config=serving_config,
                    query=search_query,
                    image_query=image_query,
                    page_size=1,
                    )

                search_result = client.search(request)
                responses.extend([str(response.document) for response in search_result])

        else:

            request = discoveryengine.SearchRequest(
                    serving_config=serving_config,
                    query=search_query,
                    page_size=1,
                    )

            search_result = client.search(request)
            responses.extend([str(response.document) for response in search_result])

        return responses