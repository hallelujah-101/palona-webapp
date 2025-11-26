import os
from dotenv import load_dotenv

from google.adk.agents import Agent
import vertexai
from vertexai import agent_engines
from google.cloud import discoveryengine
from google.adk.memory import VertexAiMemoryBankService
from google.adk.sessions import VertexAiSessionService


class AGENT:

    def __init__(self):
        """Initialises the vertex ai project and reasoning engine"""
        load_dotenv()

        PROJECT_ID = os.getenv('PROJECT_ID')
        LOCATION = os.getenv('LOCATION')
        STAGING_BUCKET = os.getenv('STAGING_BUCKET')
        AGENT_ENGINE_ID = os.getenv('AGENT_ENGINE_ID')
        AGENT_ENGINE_RESOURCE_NAME = os.getenv('AGENT_ENGINE_RESOURCE_NAME')
        
        self.agent_instruction = "You are a helpful and funny conversational agent named Gemi, and you are a Gemini. 
                            + "1. You provide users with recommendations and search results from a catalogue using the vertex_search tool. " 
                            + "2. You take user questions which may or may not contain images and if they are product related search through a database using the vertex_search tool which allows for text and image search, if they aren't product related you respond with a general response." 
                            + "3. You use the output_formatter tool to, when the response from the vertex_search tool has products, by extracting the ProductTitle, Gender, ProductId and Category fields from the result for each product" 
                            + "4. You use the output_formatter tool to form the final response for all queries and return the dictionary output from the method" 
                            + "You do not give the user details of any intermediate steps and data"
        
        vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)
        self.agent = LlmAgent(
                            model=MODEL,
                            name="catalogue_query_agent",
                            tools=[adk.tools.preload_memory_tool.PreloadMemoryTool(), self.vertex_search, self.output_formatter],
                            after_agent_callback=self.add_session_to_memory,
                            instruction=catalogue_agent_instruction,
                        )
                        
        self.session_service = VertexAiSessionService(
            project=PROJECT_ID, location=LOCATION, agent_engine_id=AGENT_ENGINE_ID
        )
        
        self.memory_service = VertexAiMemoryBankService(
            project=PROJECT_ID, location=LOCATION, agent_engine_id=AGENT_ENGINE_ID
        )
        
        self.runner = Runner(
            app_name=self.agent.name, 
            agent=self.agent,
            session_service=self.session_service,
            memory_service=self.memory_service,
        )
        
    async def add_session_to_memory(
        callback_context: CallbackContext
    ) -> Optional[types.Content]:
    """Automatically save completed sessions to memory bank """
        if hasattr(callback_context, "_invocation_context"):
            invocation_context = callback_context._invocation_context
            if invocation_context.memory_service:
                await invocation_context.memory_service.add_session_to_memory(
                    invocation_context.session
                )
    
    
    async def query(self, query, user_id): 
    
        session = await session_service.create_session(
            app_name=self.agent.name, 
            user_id=user_id,
        )
        content = types.Content(role="user", parts=[types.Part(text=query)])
        events = runner.run(
            user_id=session.user_id, session_id=session.id, new_message=content
        )

        for event in events:
            if event.is_final_response():
                final_response = event.content.parts[0].text
                return f"Agent Response: {final_response}"
                    
    
    def output_formatter(text_response: str, product_list: Optional[List]):
    """Format output using the summary response text and list of products in the agent response"""

    return {"response": text_response, "products": product_list}
        
    def vertex_search(search_query: str, images: Optional[List[str]] = []):
    """Connect to the Vertex AI Search resource and fetches search results based on the query."""
    from google.cloud import discoveryengine

    client = discoveryengine.SearchServiceClient()

    serving_config = client.serving_config_path(
        project=PROJECT_ID,
        location=LOCATION_ID,
        data_store=DATA_STORE_ID,
        serving_config=APP_ID
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