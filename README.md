# Gemi backend 

Python backend utilising Vertex Search AI and Reasoning Engine

# Getting started 
## Setting up Vertex AI Search and Reasoning Engine

This project uses Google cloud resources in the backend for searching through app data and reasoning about it. The Vertex Search AI resource allows for natural language to optimised query conversions for structured data which is ideal for the catalogue dataset used in the project and allows for image based queries. The reasoning engine processes this data and organises it for the user. Follow the steps below to setup these resources

- Create a Vertex AI Search app
  - Create a Vertex Search resource in your Google cloud account
  - [Creating a Vertex AI resource and uploading data](https://cloud.google.com/generative-ai-app-builder/docs/create-engine-es)
 
- Setting up a Firestore database for chat history
  - [Setup a firestore database through the console](https://cloud.google.com/firestore/native/docs/manage-databases)
  - Create a collection
    
- Creating and Deploying a Langchain agent
  - [Session management with firestore database](https://cloud.google.com/agent-builder/agent-engine/develop/langchain#chat-history)
  - [Agent creation and deployment](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/quickstart)
    
- Deploy to Cloud Run applications
  - [Deployment steps](https://cloud.google.com/run/docs/quickstarts/deploy-container)

Fill in all the environment variables with the corresponding values from the resources created in the [frontend ReadMe](https://github.com/hallelujah-101/paloni_flutter/blob/main/README.md) and the steps above.

         PROJECT_ID	:
         LOCATION_ID :
         STAGING_BUCKET	:
         AGENT_ENGINE_RESOURCE_NAME: 

# Running locally 

Add a .env file with values for the variables in the previous section. Then run the following commands in the terminal.

```Bash
    python3 -m venv <name>
```

```Bash
    pip install -r requirements.txt
```

```Bash
    flask run
```



