## Core Concepts of Agent Development Kit

ADK is built on several core concepts that make it a powerful and flexible framework:

* **Agent**: The fundamental building block for a specific task. Agents can use LLMs for reasoning and planning, utilize tools, and even work together on complex projects.
* **Tools**: These extend an agent's capabilities beyond simple conversation by enabling interactions with external APIs, web searches, code execution, or calling other services.
* **Session Services**: These manage the context of a single conversation, including its history (Events) and the agent's short-term working memory (State) for that conversation.
* **Callbacks**: Custom code snippets that run at specific points in the agent's process for things like checks, logging, or modifying behavior.
* **Artifact Management**: This allows agents to save, load, and manage files and binary data (like images or PDFs) associated with a session.
* **Runner**: The engine that handles the execution flow, orchestrating agent interactions based on events and coordinating with backend services.

## Empower ADK agents with tools

Agent Development Kit provides developers with a diverse range of tool options:

*   **Pre-built Tools**: Ready-to-use functionalities such as Google Search, Code Execution, and Retrieval-Augmented Generation (RAG) tools.
*   **Third-Party Tools**: Seamless integration of tools from external libraries like LangChain, CrewAI and MCP
*   **Custom Tools**: The ability to create custom tools tailored to specific requirements, by using language specific constructs and Agents-as-Tools. The SDK also provides asynchronous capabilities through Long Running Function Tools.



## Objectives

In this part of the workshop, you will create agent that can use variou tools. You will test agents in ADK’s browser UI, from a CLI chat interface.

*   The key capabilities and core concepts of Agent Development Kit (ADK)
*   How to structure project directories for ADK
*   The most fundamental parameters of agents in ADK, including how to specify model names and tools
*   Some features of ADK’s browser UI
*   How to control the output schema of an agent
*   How to run agents in three ways (via the browser UI, programmatically, and via the CLI chat interface)
*   Provide prebuilt Google, LangChain, or CrewAI tools to an agent
*   Discuss the importance of structured docstrings and typing when writing functions for agent tools
*   Write your own tool functions for an agent
*   Use an ADK agent as an MCP client to interact with tools from existing MCP servers.
*   Configure and deploy your own MCP server to expose ADK tools to other clients.
*   Connect ADK agents with external tools through standardized MCP communication.
*   Enable seamless interaction between LLMs and tools using Model Context Protocol.


## Use your IDE of choice (like VSCode) to perform the following tasks:


## Task 1. Review the structure of Agent Development Kit project directories

1.  Use your IDE to open the **adk_tools** folder. 
2.  This directory contains various other directories. Each of these directories represents a separate agent. Separating agents into their own directories within a project directory provides organization and allows Agent Development Kit to understand what agents are present.
3.  Click on the **my_google_search_agent** to explore an agent directory.
4.  Notice that the directory contains an `__init__.py` file and an `agent.py` file. An `__init__.py` file is typically used to identify a directory as a Python package that can be imported by other Python code. **Click the `init.py` file** to view its contents.
5.  Notice that the `__init__.py`file contains a single line, which imports from the `agent.py` file. ADK uses this to identify this directory as an agent package:

    ```python
    from . import agent
    ```
6.  Now click on the `agent.py` file. This file consists of a simple agent. You will equip it with a powerful tool: the ability to search the internet using Google Search. Notice a few things about the file:
    *   Notice the imports from `google.adk`: the `Agent` class and the `google_search` tool from the `tools` module
    *   Read the code comments that describe the parameters that configure this simple agent.
7.  To use the imported `google_search` tool, it needs to be passed to the agent. Do that by **pasting the following line** into the `agent.py` file where indicated at the end of the `Agent` object creation:

    ```python
    tools=[google_search]
    ```
8.  **Save** the file.

> **Note:** Tools enable an agent to perform actions beyond generating text. In this case, the `google_search` tool allows the agent to decide when it would like more information than it already has from its training data. It can then write a search query, use Google Search to search the web, and then base its response to the user on the results. When a model bases its response on additional information that it retrieves, it is called "grounding," and this overall process is known as "retrieval-augmented generation" or "RAG."

## Task 2. Run the agent using the ADK's Dev UI

1. In the Cloud Shell Terminal, ensure you are in the **adk_project** directory where your agent subdirectories are located by running:

    ```bash
    cd adk_tools
    ```
2. **Launch the Agent Development Kit Dev UI** with the following command:

    ```bash
    adk web
    ```
    **Output**
    ```bash
     INFO:   Started server process [2434]
     INFO:   Waiting for application startup.
     +-------------------------------------------------------+
     | ADK Web Server started                                |
     |                                                       |
     | For local testing, access at http://localhost:8000.   |
     +-------------------------------------------------------+

     INFO:   Application startup complete.
     INFO:   Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    ```
3. To view the web interface in a new tab, click the **http://127.0.0.1:8000** link in the Terminal output.
4. A new browser tab will open with the ADK Dev UI.
5. From the **Select an agent** dropdown on the left, select **my_google_search_agent**.


6. In the chat input field in the bottom right, begin the conversation with:

    ```bash
    hello
    ```
7. The agent should respond. In order to encourage the agent to use its Google Search tool, enter the question:

    ```bash
    What is some recent global news?
    ```
    or
    ```
    what are some new movies that have been released in the past month?
    ```
8. You will notice from the results that the agent is able to use Google Search to get up-to-date information, rather than having its information stop on the date when its model was trained.

    > **Important note:** When you use grounding with Google Search, you are [required to display these suggestions](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/grounding-search-suggestions), which help users follow up on the information the model used for its response.
9. Click the agent icon next to the agent's response (or an event from the list on the **Events** pane) to inspect the event returned by the agent, which includes the `content` returned to the user and `grounding_metadata` which details the search results that the response was based on.
10. When you are finished exploring the dev UI, close this browser tab and return to your browser tab with the Cloud Shell Terminal, click on the terminal's pane, and press `CTRL + C` to stop the web server.






## Task 3. Use a LangChain Tool

The LangChain community has created a [large number of tool integrations](https://python.langchain.com/docs/integrations/tools/) to access many sources of data, integrate with various web products, and accomplish many things. Using community tools within ADK can save you rewriting a tool that someone has already created.

1.  Use your IDE to navigate to the directory **adk_tools/langchain_tool_agent**.

2.  Click on the **agent.py** file in the **langchain_tool_agent** directory.
5.  Notice the import of the `LangchainTool` class from ADK. This is a wrapper class that allows you to use LangChain tools within Agent Development Kit.
6.  **Add the following code** where indicated in the `agent.py` file to add the [LangChain Wikipedia tool](https://python.langchain.com/docs/integrations/tools/wikipedia/) to your agent. This will allow your agent to search for information on [Wikipedia](https://www.wikipedia.org/):

    ```python
    tools = [
        # Use the LangchainTool wrapper...
        LangchainTool(
          # to pass in a LangChain tool.
          # In this case, the WikipediaQueryRun tool,
          # which requires the WikipediaAPIWrapper as
          # part of the tool.
          tool=WikipediaQueryRun(
            api_wrapper=WikipediaAPIWrapper()
          )
        )
      ]
    ```
7.  **Save** the file.
8.  You will run this agent using the dev UI to see how its tools allow you to easily visualize tool requests and responses. From the **adk_tools** project directory, launch the agent with the ADK command line UI with:

    ```bash
    adk web
    ```
9.  Click the **http://127.0.0.1:8000** link in the Terminal output.
10. A new browser tab will open with the ADK Dev UI.
11. From the **Select an agent** dropdown on the left, select the **langchain_tool_agent** from the dropdown.
12. Query the agent with:

    ```bash
    Who was Grace Hopper?
    ```
14. Click the agent icon next to the agent's chat bubble indicating the use of the **wikipedia** tool.
15. Notice that the content includes a `functionCall` with the query to Wikipedia.
16. At the top of the tab, click the **forward button** to move to the next event.
17. On the **Request** tab, you can see the result retrieved from Wikipedia used to generate the model's response.
18. When you are finished asking questions of this agent, close the dev UI browser tab.
19. In the Terminal, press **CTRL + C** to stop the server.





## **What is Model Context Protocol (MCP)**

Model Context Protocol (MCP) is an open standard designed to standardize how Large Language Models (LLMs) like Gemini and Claude communicate with external applications, data sources, and tools. Think of it as a universal connection mechanism that simplifies how LLMs obtain context, execute actions, and interact with various systems.

MCP follows a client-server architecture, defining how data (resources), interactive templates (prompts), and actionable functions (tools) are exposed by an MCP server and consumed by an MCP client (which could be an LLM host application or an AI agent).

We cover two primary integration patterns:

*   Using Existing MCP Servers within ADK: An ADK agent acts as an MCP client, leveraging tools provided by external MCP servers.
*   Exposing ADK Tools via an MCP Server: Building an MCP server that wraps ADK tools, making them accessible to any MCP client.




## Task 4. Using Google Maps MCP server with ADK agents (ADK as an MCP client) in adk web

This section demonstrates how to integrate tools from an external Google Maps MCP server into your ADK agents. This is the most common integration pattern when your ADK agent needs to use capabilities provided by an existing service that exposes an MCP interface. You will see how the `MCPToolset` class can be directly added to your agent's `tools` list, enabling seamless connection to an MCP server, discovery of its tools, and making them available for your agent to use. These examples primarily focus on interactions within the `adk web` development environment.

### MCP Toolset

The `MCPToolset` class is ADK's primary mechanism for integrating tools from an MCP server. When you include an `MCPToolset` instance in your agent's `tools` list, it automatically handles the interaction with the specified MCP server. Here's how it works:

*   **Connection Management**: On initialization, `MCPToolset` establishes and manages the connection to the MCP server. This can be a local server process (using `StdioServerParameters` for communication over standard input/output) or a remote server (using `SseServerParams` for Server-Sent Events). The toolset also handles the graceful shutdown of this connection when the agent or application terminates.
*   **Tool Discovery & Adaptation**: Once connected, `MCPToolset` queries the MCP server for its available tools (via the `list_tools` MCP method). It then converts the schemas of these discovered MCP tools into ADK-compatible `BaseTool` instances.
*   **Exposure to Agent**: These adapted tools are then made available to your `LlmAgent` as if they were native ADK tools.
*   **Proxying Tool Calls**: When your `LlmAgent` decides to use one of these tools, `MCPToolset` transparently proxies the call (using the `call_tool` MCP method) to the MCP server, sends the necessary arguments, and returns the server's response back to the agent.
*   **Filtering (Optional)**: You can use the `tool_filter` parameter when creating an MCPToolset to select a specific subset of tools from the MCP server, rather than exposing all of them to your agent.

### Get API key and Enable APIs

In this sub-section, you will generate a new API key named **GOOGLE_MAPS_API_KEY**.

1.  **Open the browser tab displaying the Google Cloud Console** 
2.  Search for **Credentials** in the search bar at the top of the page. Select it from the results.
3.  On the **Credentials** page, click **+ Create Credentials** at the top of the page, then select **API key**.
    The **API key created** dialog will display your newly created API key. Be sure to save this key locally for later use in the lab.
4.  Click **Close** on the dialog box.
    Your newly created key will be named **API Key 1** by default. Select the key, rename it to **GOOGLE_MAPS_API_KEY**, and click **Save**.
5.  Double check that **Directions API** is enabled.

### Define your Agent with an MCP Toolset for Google Maps

In this sub-section, you will configure your agent to use the `MCPToolset` for Google Maps, enabling it to seamlessly provide directions and location-based information.

1.  Using your IDE find the **.env** file and update the  `YOUR_ACTUAL_API_KEY` value with the Google Maps API key you generated and saved in a previous step:
2.  Click on the **agent.py** file in the **google_maps_mcp_agent** directory.
3.  Notice the import of the `MCPToolset` class from ADK, along with `StdioConnectionParams` and `StdioServerParameters`. These are used to connect to an MCP server.
4.  Add the following code where indicated in the `agent.py` file to add the Google Maps tool to your agent:

    ```
    tools=[
        MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command='npx',
                args=[
                    "-y",
                    "@modelcontextprotocol/server-google-maps",
                ],
                env={
                    "GOOGLE_MAPS_API_KEY": google_maps_api_key
                }
            ),
            timeout=15,
            ),
        )
    ],
    ```
9.  **Save** the file.
10. From the **adk_tools** project directory, **launch the Agent Development Kit Dev UI** with the following command:

    ```bash
    adk web
    ```
11. **Output:**
    ```bash
    INFO:   Started server process [2434]
    INFO:   Waiting for application startup.
    +----------------------------------------------------+
    | ADK Web Server started                             |
    |                                                    |
    | For local testing, access at http://localhost:8000.   |
    +----------------------------------------------------+

    INFO:   Application startup complete.
    INFO:   Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    ```
12. To view the web interface in a new tab, click the **http://127.0.0.1:8000** link in the Terminal output.
13. A new browser tab will open with the ADK Dev UI. From the **Select an agent** dropdown on the left, select the **google_maps_mcp_agent** from the dropdown.
14. Query the agent with:

    ```bash
    Get directions from GooglePlex to SFO.
    ```
   
15. **Click the agent icon** next to the agent's chat bubble with a lightning bolt, which indicates a function call. This will open up the Event inspector for this event:

16. **Notice that agent graph indicates several different tools**, identified by the wrench emoji (🔧). Even though you only imported one `MCPToolset`, that tool set came with the different tools you see listed here, such as `maps_place_details` and `maps_directions`.

17. On the **Request** tab, you can see the structure of the request. You can use the arrows at the top of the Event inspector to browse the agent's thoughts, function calls, and responses.
18. When you are finished asking questions of this agent, close the dev UI browser tab.
19. In the Terminal, press **CTRL + C** to stop the server.

## Task 5. Building an MCP server with ADK tools (MCP server exposing ADK)

In this section, you'll learn how to expose the ADK `load_web_page` tool through a custom-built MCP server. This pattern allows you to wrap existing ADK tools and make them accessible to any standard MCP client application.

### Create the MCP Server Script and Implement Server Logic

1.  In your IDE, find the **adk_tools** folder. Click it to toggle it open.
2.  Navigate to the directory **adk_tools/adk_mcp_server**.
3.  A Python file named **adk_server.py** has been prepared and commented for you. **Take some time to review that file**, reading the comments to understand how the code wraps a tool and serves it as an MCP server. Notice how it allows MCP clients to list available tools as well as invoke the ADK tool asynchronously, handling requests and responses in an MCP-compliant format.

### Test the Custom MCP Server with an ADK Agent

1.  Click on the **agent.py** file in the **adk_mcp_server** directory.
2.  Check the path to your **adk_server.py** file.
5.  Next, add the following code where indicated in the `agent.py` file to add the ADK `load_web_page` tool to your agent:

    ```python
      tools=[
        MCPToolset(
        connection_params=StdioConnectionParams(
          server_params=StdioServerParameters(
            command="python3", # Command to run your MCP server script
            args=[
              PATH_TO_YOUR_MCP_SERVER_SCRIPT, # Argument is the path to the script
            ],
            env={
              "GOOGLE_MAPS_API_KEY": google_maps_api_key
            }
          ),
          timeout=15,
          ),
        )
      ],
    ```
6.  **Save** the file.
7.  To run the MCP server, start the `adk_server.py` script by running the following command in Terminal:

    ```bash
    python3 ~/adk_workshop/adk_tools/adk_mcp_server/adk_server.py
    ```

9.  Open a Terminal and from the **adk_tools** project directory, launch the **Agent Development Kit Dev UI** with the following command:

    ```bash
    cd ~/adk_workshop/adk_tools
    adk web
    ```
11. Click the **http://127.0.0.1:8000** link to open the ADK Dev UI.
12. From the **Select an agent** dropdown on the left, select the **adk_mcp_server** from the dropdown.
13. Query the agent with:

    ```bash
    Load the content from https://example.com
    ```

15. What happens here:
    *   The ADK agent (`web_reader_mcp_client_agent`) uses the `MCPToolset` to connect to your `adk_server.py`.
    *   The MCP server will receive the `call_tool` request, execute the ADK `load_web_page` tool, and return the result.
    *   The ADK agent will then relay this information. You should see logs from both the ADK Web UI (and its terminal) and from your `adk_server.py` terminal in the Cloud Shell Terminal tab where it is running.
16. This demonstrates that ADK tools can be encapsulated within an MCP server, making them accessible to a broad range of MCP-compliant clients including ADK agents.

---------

# A2A Human-in-the-Loop Sample Agent

This sample demonstrates the **Agent-to-Agent (A2A)** architecture with **Human-in-the-Loop** workflows in the Agent Development Kit (ADK). The sample implements a reimbursement processing agent that automatically handles small expenses while requiring remote agent to process for larger amounts. The remote agent will require a human approval for large amounts, thus surface this request to local agent and human interacting with local agent can approve the request.

## Overview

The A2A Human-in-the-Loop sample consists of:

- **Root Agent** (`root_agent`): The main reimbursement agent that handles expense requests and delegates approval to remote Approval Agent for large amounts
- **Approval Agent** (`approval_agent`): A remote A2A agent that handles the human approval process via  long-running tools (which implements asynchronous approval workflows that can pause execution and wait for human input), this agent is running on a separate A2A server


## Architecture

```
┌─────────────────┐    ┌────────────────────┐    ┌──────────────────┐
│   Human Manager │───▶│   Root Agent       │───▶│   Approval Agent │
│   (External)    │    │    (Local)         │    │  (Remote A2A)    │
│                 │    │                    │    │ (localhost:8001) │
│   Approval UI   │◀───│                    │◀───│                  │
└─────────────────┘    └────────────────────┘    └──────────────────┘
```

## Key Features

### 1. **Automated Decision Making**
- Automatically approves reimbursements under $100
- Uses business logic to determine when human intervention is required
- Provides immediate responses for simple cases

### 2. **Human-in-the-Loop Workflow**
- Seamlessly escalates high-value requests (>$100) to remote approval agent
- Remote approval agent uses long-running tools to surface approval requests back to the root agent
- Human managers interact directly with the root agent to approve/reject requests

### 3. **Long-Running Tool Integration**
- Demonstrates `LongRunningFunctionTool` for asynchronous operations
- Shows how to handle pending states and external updates
- Implements proper tool response handling for delayed approvals

### 4. **Remote A2A Agent Communication**
- The approval agent runs as a separate service that processes approval workflows
- Communicates via HTTP at `http://localhost:8001/a2a/human_in_loop`
- Surfaces approval requests back to the root agent for human interaction

## Setup and Usage

### Prerequisites

1. **Start the Remote Approval Agent server**:
   ```bash
   # Start the remote a2a server that serves the human-in-the-loop approval agent on port 8001
   adk api_server --a2a --port 8001 adk_multiagent_systems/a2a_human_in_loop/remote_a2a
   ```

2. **Run the Main Agent**:
   ```bash
   # In a separate terminal, run the adk web server (verify that you're in the same virtual environment, if not run "source .venv/bin/activate" )
   adk web adk_multiagent_systems/
   ```

### Example Interactions

Once both services are running, you can interact with the root agent through the approval workflow:

**Automatic Approval (Under $100):**
```
User: Please reimburse $50 for meals
Agent: I'll process your reimbursement request for $50 for meals. Since this amount is under $100, I can approve it automatically.
Agent: ✅ Reimbursement approved and processed: $50 for meals
```

**Human Approval Required (Over $100):**
```
User: Please reimburse $200 for conference travel
Agent: I'll process your reimbursement request for $200 for conference travel. Since this amount exceeds $100, I need to get manager approval.
Agent: 🔄 Request submitted for approval (Ticket: reimbursement-ticket-001). Please wait for manager review.
[Human manager interacts with root agent to approve the request]
Agent: ✅ Great news! Your reimbursement has been approved by the manager. Processing $200 for conference travel.
```

## Code Structure

### Main Agent (`agent.py`)

- **`reimburse(purpose: str, amount: float)`**: Function tool for processing reimbursements
- **`approval_agent`**: Remote A2A agent configuration for human approval workflows
- **`root_agent`**: Main reimbursement agent with automatic/manual approval logic

### Remote Approval Agent (`remote_a2a/human_in_loop/`)

- **`agent.py`**: Implementation of the approval agent with long-running tools
- **`agent.json`**: Agent card of the A2A agent

- **`ask_for_approval()`**: Long-running tool that handles approval requests

## Long-Running Tool Workflow

The human-in-the-loop process follows this pattern:

1. **Initial Call**: Root agent delegates approval request to remote approval agent for amounts >$100
2. **Pending Response**: Remote approval agent returns immediate response with `status: "pending"` and ticket ID and serface the approval request to root agent
3. **Agent Acknowledgment**: Root agent informs user about pending approval status
4. **Human Interaction**: Human manager interacts with root agent to review and approve/reject the request
5. **Updated Response**: Root agent receives updated tool response with approval decision and send it to remote agent
6. **Final Action**: Remote agent processes the approval and completes the reimbursement and send the result to root_agent

## Extending the Sample

You can extend this sample by:

- Adding more complex approval hierarchies (multiple approval levels)
- Implementing different approval rules based on expense categories
- Creating additional remote agent for budget checking or policy validation
- Adding notification systems for approval status updates
- Integrating with external approval systems or databases
- Implementing approval timeouts and escalation procedures

## Troubleshooting

**Connection Issues:**
- Ensure the local ADK web server is running on port 8000
- Ensure the remote A2A server is running on port 8001
- Check that no firewall is blocking localhost connections
- Verify the agent card URL passed to RemoteA2AAgent constructor matches the running A2A server

**Agent Not Responding:**
- Check the logs for both the local ADK web server on port 8000 and remote A2A server on port 8001
- Verify the agent instructions are clear and unambiguous
- Ensure long-running tool responses are properly formatted with matching IDs

**Approval Workflow Issues:**
- Verify that updated tool responses use the same `id` and `name` as the original function call
- Check that the approval status is correctly updated in the tool response
- Ensure the human approval process is properly simulated or integrated
