# Gemi backend 

Python backend utilising Vertex Search AI and Reasoning Engine

# Getting started
## Setting up Vertex AI Search and Reasoning Engine

This project uses Google cloud resources in the backend for searching through app data and reasoning about it. Follow the steps below to setup these resources

- Create a Vertex AI Search app
  - Once in the Google cloud account head to the console and create a Vertex Search resource 
  - [Creating a Vertex AI resource and uploading data](https://cloud.google.com/generative-ai-app-builder/docs/create-engine-es)

- Creating and Deploying a Langchain agent
  - [Creating an agent and deploying it](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/quickstart)


Then deploy this application to Cloud Run App. Fill in all the environment variables with the corresponding values from the resources created in the ReadMe frontend and the steps above.


# Running the app 

```Bash
    python3 -m venv <name>
```

```Bash
    pip install -r requirements.txt
```

```Bash
    flask run
```



