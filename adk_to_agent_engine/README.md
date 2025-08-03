```markdown
# Deploy ADK agents to Agent Engine

Learn to deploy ADK agents to Agent Engine for a scalable, fully managed environment for your agentic workflows, so you can focus on the agents' logic while infrastructure is allocated and scaled for you.

## Objective
* Benefits of deploying agents, especially multi-agent systems, to Agent Engine
* How to wrap an agent to deploy it to Agent Engine
* How to test an agent locally before deploying
* How to query an agent deployed to Agent Engine
* How to list and delete agents

## Agent Engine
**Vertex AI Agent Engine** (formerly known as LangChain on Vertex AI or Vertex AI Reasoning Engine) is a fully managed Google Cloud service enabling developers to deploy, manage, and scale AI agents in production.
You can learn more about its benefits in the [Vertex AI Agent Engine documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview).



   python3 -m pip install google-adk==1.6.1 --upgrade --force-reinstall

## Task 1. Deploy your agent app to Agent Engine
1. To create a script to deploy your app to Agent Engine, right-click on the **transcript_summarization_agent** directory and select **New File...**.
2. Name the file `deploy_to_agent_engine.py`.
3. In this file, paste the following code:
   ```python
import os
import vertexai
from vertexai import agent_engines
from dotenv import load_dotenv

from agent import root_agent

load_dotenv()

vertexai.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
    staging_bucket="gs://" + os.getenv("GOOGLE_CLOUD_PROJECT")+"-bucket",
)

remote_app = agent_engines.create(
    display_name=os.getenv("APP_NAME", "Agent App"),
    agent_engine=root_agent,
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]"
    ]
)
   ```
4. Save the file.
5. Review this script as well. Once again, your **root_agent** is imported, but this time it is deployed to Agent Engine with the `agent_engines.create()` method. Behind the scenes, your agent will again be wrapped to handle user sessions.
6. Run this file from the **transcript_summarization_agent** directory with:
   ```bash
   python3 deploy_to_agent_engine.py
   ```
   Deployment should take about 10-15 minutes. You can follow the status from the log file that will be linked from the command's output. During that time, the following steps are occurring:
    * A bundle of artifacts is generated locally, comprising:
        * `*.pkl`: a pickle file corresponding to local_agent.
        * `requirements.txt`: a text file containing the [package requirements](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/deploy#package-requirements).
        * `dependencies.tar.gz`: a tar file containing any [extra packages](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/deploy#extra-packages).
    * The bundle is uploaded to Cloud Storage (using a defined [directory](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/deploy#gcs-directory) if specified) for staging the artifacts.
    * The Cloud Storage URIs for the respective artifacts are specified in the [PackageSpec](https://cloud.google.com/vertex-ai/generative-ai/docs/reference/rest/v1/projects.locations.reasoningEngines#PackageSpec).
    * The Vertex AI Agent Engine service receives the request and builds containers and spins up HTTP servers on the backend.
7. Agent Engine is now available to Preview in the Google Cloud Console. When your agent has completed its deployment, return to your Cloud Console tab and search **Agent Engine** in the search bar at the top. Select your **location** and you will see your deployed agent. You can click on its name to explore metrics and sessions that will populate as your agent is used.

## Task 2. Import a class to wrap your agent and test it locally
1. Using your IDE, navigate to the **adk_to_agent_engine/transcript_summarization_agent** directory.
2. Click on the **agent.py** file to review the instructions of this simple summarization agent.
   ```python
   root_agent = Agent(
       name="transcript_summarization_agent",
       description="Summarizes chat transcripts.",
       model=os.getenv("MODEL", "gemini-2.0-flash-exp"),
       instruction="Summarize the provided chat transcript.",
   )
   ```
8. An agent deployed to Agent Engine needs to be able to act as a web app that can create and retrieve user sessions from its session service. To see this locally, right-click on the **transcript_summarization_agent** directory and select **New File...**.
9. Name the file `test_agent_app_locally.py`.
10. In this file, paste the following code:
    ```python
import logging
import google.cloud.logging
import asyncio

from vertexai.preview import reasoning_engines

from agent import root_agent

logging.basicConfig(level=logging.INFO)
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

async def main():

    agent_app = reasoning_engines.AdkApp(
        agent=root_agent,
        enable_tracing=True,
    )

    session = agent_app.create_session(user_id="u_123")

    for event in agent_app.stream_query(
        user_id="u_123",
        session_id=session.id,
        message="""
            Virtual Agent: Hi, I am a vehicle sales agent. How can I help you?
            User: I'd like to buy a car.
            Virtual Agent: Can I interest you in a boat?
            User: No, a car.
            Virtual Agent: This boat will be $10,000.
            User: Goodbye.
            """,
    ):
        logging.info("[local test] " + event["content"]["parts"][0]["text"])
        cloud_logging_client.flush_handlers()

if __name__ == "__main__":
    asyncio.run(main())
    ```
11. Review the code above. Notice that your **root_agent** is imported from your **agent.py** file. This script then uses the class `reasoning_engines.AdkApp` to wrap your agent in order for it to act as a web app which can handle the creation and management of user sessions.
12. Read the transcript that is passed as input so that you can determine if the agent did a good job summarizing it. (The Agent Development Kit can help you be more systematic in evaluating your ADK agents, but that is a topic for another lab.)
13. **Save** the file.
14. This file will execute the `stream_query()` method of the `reasoning_engines.AdkApp` class locally. To run it, paste and run this command in the Cloud Shell Terminal:
    ```bash
    cd ~/adk_workshop/adk_to_agent_engine/transcript_summarization_agent
    python3 test_agent_app_locally.py
    ```
    **Example output (yours may be a little different):**
    ```bash
    The user contacted a virtual agent to buy a car, but the agent repeatedly tried to sell the user a boat instead. The user ended the conversation.
    ```

## Task 4. Get and query an agent deployed to Agent Engine
1. For your agent to be able to use models and manage sessions through Vertex AI, you'll need to grant the Agent Engine service agent permissions. Navigate to **IAM** in the console.
2. Click the checkbox to **Include Google-provided role grants**.
3. Find the **AI Platform Reasoning Engine Service Agent** (`service-PROJECT_NUMBER@gcp-sa-aiplatform-re.iam.gserviceaccount.com`) and click the pencil icon in its row.
4. Click **Add another role**.
5. Select **Vertex AI User**.
6. Click **Save**.
7. Back in your IDE, browse to **transcript_summarization_agent** directory and open file `query_app_on_agent_engine.py`.
11. Review the commented code to pay attention to what it is doing.
12. Review the transcript passed to the agent, so that you can evaluate if it's generating an adequate summary.
13. Run the file from the **transcript_summarization_agent** directory with:
    ```bash
    python3 query_app_on_agent_engine.py
    ```
    **Example output (yours may be a little different):**
    ```bash
    The user wants to buy a boat and has a budget of $50,000. The virtual agent confirmed that this budget is sufficient for a "very nice boat" and the user is ready to proceed with the purchase.
    ```