# Palona backend 

Python backend utilising Vertex Search AI and Reasoning Engine

# Getting started
## Setting up Vertex AI Search and 

This project uses Google cloud resources in the backend for searching through app data and reasoning about it. Follow the steps below to setup these resources

- Create a Vertex AI Search app
  - Once in the Google cloud account head to the console and create a Vertex Search resource 
  - [Creating a Vertex AI resource and uploading data](https://cloud.google.com/generative-ai-app-builder/docs/create-engine-es)

- Creating and Deploying a Langchain agent
  - [Creating an agent and deploying it](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/quickstart)
  - Place the ID of the Reasoning Engine in the 'NB_R_ENGINE_ID' variable

Fill in all the variables with the corresponding values from the resources created in the ReadMe frontend.

# Running the app 

Create a virtual environment

```Bash
    pip install -r requirements.txt
```

```Bash
    flask run
```



