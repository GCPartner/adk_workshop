
## Objectives

In this lab, you will create a single agent that can use a search tool. You will test agents in ADK’s browser UI, from a CLI chat interface, and programmatically from within a script.

You will consider:

*   The key capabilities of Agent Development Kit
*   The core concepts of ADK
*   How to structure project directories for ADK
*   The most fundamental parameters of agents in ADK, including how to specify model names and tools
*   Some features of ADK’s browser UI
*   How to control the output schema of an agent
*   How to run agents in three ways (via the browser UI, programmatically, and via the CLI chat interface)

## Use your IDE of choice (like VSCode) to perform the following tasks:


## Task 1. Install ADK and set up your environment

### Configure GCP Project details

### Enable Vertex AI recommended APIs

1. Step 3 from this [guide](https://cloud.google.com/vertex-ai/docs/start/cloud-environment#set_up_a_project)


### Download and install the ADK and code samples for this lab

1.  **Install ADK**

    ```bash
    sudo python3 -m pip install google-adk==1.6.1
    ```
2.  Install requirements with:

    ```bash
    sudo python3 -m pip install -r adk_project/requirements.txt
    ```


## Task 2. Review the structure of Agent Development Kit project directories

1.  Use your IDE to open the **adk_project** folder. Click it to toggle it open.
2.  This directory contains three other directories: **my_google_search_agent**, **app_agent**, and **llm_auditor**. Each of these directories represents a separate agent. Separating agents into their own directories within a project directory provides organization and allows Agent Development Kit to understand what agents are present.
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

## Task 3. Run the agent using the ADK's Dev UI

1.  Navigate to the **adk_project/my_google_search_agent** directory.
2. Select the **.env** file in the **my_google_search_agent** directory.
3. Paste these values over what is currently in the file to **update the file to include your project ID**:

    ```ini
    GOOGLE_GENAI_USE_VERTEXAI=TRUE
    GOOGLE_CLOUD_PROJECT=YOUR_PROJECT
    GOOGLE_CLOUD_LOCATION=us-central1
    MODEL=gemini-2.0-flash-001
    ```
4. **Save** the file.

    > **Note:** These variables play the following roles:
    > *   `GOOGLE_GENAI_USE_VERTEXAI=TRUE` indicates that you will use Vertex AI for authentication as opposed to Gemini API key authentication.
    > *   `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` provide the project and location with which to associate your model calls.
    > *   `MODEL` is not required, but is stored here so that it can be loaded as another environment variable. This can be a convenient way to try different models in different deployment environments.
    >
    > When you test your agent using ADK's dev UI or the command-line chat interface, they will load and use an agent's `.env` file if one is present or else look for environment variables with the same names as those set here.
5. In the Cloud Shell Terminal, ensure you are in the **adk_project** directory where your agent subdirectories are located by running:

    ```bash
    cd ~/adk_project
    ```
15. **Launch the Agent Development Kit Dev UI** with the following command:

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
16. To view the web interface in a new tab, click the **http://127.0.0.1:8000** link in the Terminal output, which will link you via proxy to this app running locally on your Cloud Shell instance.
17. A new browser tab will open with the ADK Dev UI.
18. From the **Select an agent** dropdown on the left, select **my_google_search_agent**.


19. In the chat input field in the bottom right, begin the conversation with:

    ```bash
    hello
    ```
20. The agent should respond. In order to encourage the agent to use its Google Search tool, enter the question:

    ```bash
    What is some recent global news?
    ```
21. You will notice from the results that the agent is able to use Google Search to get up-to-date information, rather than having its information stop on the date when its model was trained.

    > **Important note:** When you use grounding with Google Search, you are [required to display these suggestions](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/grounding-search-suggestions), which help users follow up on the information the model used for its response.
22. Click the agent icon (![agent_icon](https://www.cloudskillsboost.google/focuses/126142?catalog_rank=%7B%22rank%22%3A3%2C%22num_filters%22%3A0%2C%22has_search%22%3Atrue%7D&parent=catalog&search_id=49852970#step8)) next to the agent's response (or an event from the list on the **Events** pane) to inspect the event returned by the agent, which includes the `content` returned to the user and `grounding_metadata` which details the search results that the response was based on.
23. When you are finished exploring the dev UI, close this browser tab and return to your browser tab with the Cloud Shell Terminal, click on the terminal's pane, and press `CTRL + C` to stop the web server.



## Task 4. Run an agent programmatically

While the dev UI is great for testing and debugging, it is not suitable for presenting your agent to multiple users in production.

To run an agent as part of a larger application, you will need to include a few additional components in your **agent.py** script that the web app handled for you in the previous task. Proceed with the following steps to open a script with these components to review them.

1.  Run the following commands to export environment variables. You can use this approach to set environment variables for all of your agents to use if they do not have a `.env` file in their directory:

    ```bash
    TO DO
    export GOOGLE_GENAI_USE_VERTEXAI=TRUE
    export GOOGLE_CLOUD_PROJECT=YOUR PROJECT
    export GOOGLE_CLOUD_LOCATION=us-central1
    export MODEL=gemini-2.0-flash-001
    ```
2.  In the Cloud Shell Editor file browser, select the **adk_project/app_agent** directory.
3.  Select the **agent.py** file in this directory.
4.  This agent is designed to run as part of an application. Read the commented code in **agent.py**, paying particular attention to the following components in the code:

    | Component                                 | Feature                       | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
    | :---------------------------------------- | :---------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `InMemoryRunner()`                        | Oversight of agent execution  | The Runner is the code responsible for receiving the user's query, passing it to the appropriate agent, receiving the agent's response event and passing it back to the calling application or UI for rendering, and then triggering the following event. You can read more in the ADK [documentation about the event loop](https://google.github.io/adk-docs/runtime/#the-heartbeat-the-event-loop-inner-workings).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
    | `runner.session_service.create_session()` | Conversation history & shared state | Sessions allow an agent to preserve state, remembering a list of items, the current status of a task, or other 'current' information. This class creates a local session service for simplicity, but in production this could be handled by a database.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
    | `types.Content()` and `types.Part()`      | Structured, multimodal messages | Instead of a simple string, the agent is passed a Content object which can consist of multiple Parts. This allows for complex messages, including text and multimodal content to be passed to the agent in a specific order.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

    > When you ran the agent in the dev UI, it created a session service, artifact service, and runner for you. When you write your own agents to deploy programmatically, it is recommended that you provide these components as external services rather than relying on in-memory versions.

5.  Notice that the script includes a hardcoded query, which asks the agent: `"What is the capital of France?"`
6.  Run the following command in the Cloud Shell Terminal to run this agent programmatically:

    ```bash
    python3 app_agent/agent.py
    ```
    **Selected Output**
    ```
    trivia_agent: The capital of France is Paris.
    ```
7.  You can also define specific input and/or output schema for an agent.
8.  You will now add imports for the [Pydantic schema classes](https://docs.pydantic.dev/1.10/usage/schema/) `BaseModel` and `Field` and use them to define a schema class consisting of just one field, with a key of "capital" and a string value intended for the name of a country's capital city. You can paste these lines into your **app_agent/agent.py** file, just after your other imports:

    ```python
    from pydantic import BaseModel, Field

    class CountryCapital(BaseModel):
      capital: str = Field(description="A country's capital.")
    ```

>**Important note:** When you define an output schema, you cannot use tools or agent transfers.

9.  Within your `root_agent`'s `Agent` definition, add these parameters to disable transfers (as you are required to do when using an output schema) and to set the output to be generated according to the `CountryCapital` schema you defined above:

    ```bash
        disallow_transfer_to_parent=True,
        disallow_transfer_to_peers=True,
        output_schema=CountryCapital,
    ```
10. Run the agent script again to see the response following the `output_schema`:

    ```bash
    python3 app_agent/agent.py
    ```
    **Selected Output**
    ```
    trivia_agent: {
     "capital": "Paris"
    }
    ```

Click **Check my progress** to verify the objective.

## Task 5. Chat with an agent via the command-line interface

You can also chat with an agent in your local development environment by using the command line interface. This can be very handy for quickly debugging and testing agents as you develop them.

To run an interactive session using the command line interface:

1.  **Run** the following in Cloud Shell Terminal:

    ```bash
    adk run my_google_search_agent
    ```
    **Output**:
    ```bash
    Log setup complete: /tmp/agents_log/agent.20250322_010300.log
    To access latest log: tail -F /tmp/agents_log/agent.latest.log
    Running agent basic_search_agent, type exit to exit.
    user:
    ```
2.  Input the following message:

    ```sql
    what are some new movies that have been released in the past month in India?
    ```
3.  **Example output (yours may be a little different)**:
    ```applescript
    [google_search_agent]: Here are some movies that have been released in India in the past month (approximately since April 20, 2025, given the current date of May 20, 2025):

    *   **Raid 2:** Released on May 1, 2025. It's an action, crime, and thriller film starring Ajay Devgn, Vaani Kapoor, and Riteish Deshmukh.
    *   **Kapkapiii:** Released on May 23, 2025. It is a comedy, horror film starring Shreyas Talpade and Tusshar Kapoor.
    *   **Sister Midnight:** Released on May 23, 2025. It is a comedy, drama starring Radhika Apte.
    ...
    ```
4.  When you are finished chatting with the command line interface, enter `exit` at the next user prompt to end the chat.


# Empower ADK agents with tools


## Objectives

After this lab, you will be able to:

*   Provide prebuilt Google, LangChain, or CrewAI tools to an agent
*   Discuss the importance of structured docstrings and typing when writing functions for agent tools
*   Write your own tool functions for an agent


## Tool use with the Agent Developer Kit

Agent Development Kit provides developers with a diverse range of tool options:

*   **Pre-built Tools**: Ready-to-use functionalities such as Google Search, Code Execution, and Retrieval-Augmented Generation (RAG) tools.
*   **Third-Party Tools**: Seamless integration of tools from external libraries like LangChain and CrewAI.
*   **Custom Tools**: The ability to create custom tools tailored to specific requirements, by using language specific constructs and Agents-as-Tools. The SDK also provides asynchronous capabilities through Long Running Function Tools.


## Available Pre-Built Tools from Google

Google provides several useful tools for your agents. They include:

**Google Search** (`google_search`): Allows the agent to perform web searches using Google Search. You simply add `google_search` to the agent's tools.

**Code Execution** (`built_in_code_execution`): This tool allows the agent to execute code, to perform calculations, data manipulation, or interact with other systems programmatically. You can use the pre-built `VertexCodeInterpreter` or any code executor that implements the `BaseCodeExecutor` interface.

**Retrieval** (`retrieval`): A package of tools designed to fetch information from various sources.

**Vertex AI Search Tool** (`VertexAiSearchTool`): This tool integrates with Google Cloud's Vertex AI Search service to allow the agent to search through your AI Applications data stores.


## Third-Party Tools

ADK allows you to use tools available from third-party AI libraries like LangChain and CrewAI.

## Task 3. Use a LangChain Tool

The LangChain community has created a [large number of tool integrations](https://python.langchain.com/docs/integrations/tools/) to access many sources of data, integrate with various web products, and accomplish many things. Using community tools within ADK can save you rewriting a tool that someone has already created.

1.  Use your IDE to navigate to the directory **adk_tools/langchain_tool_agent**.
2.  Write a **.env** file to provide authentication details for this agent directory by running the following in the Cloud Shell Terminal:

    ```bash
    cd ~/adk_tools
    cat << EOF > langchain_tool_agent/.env
    GOOGLE_GENAI_USE_VERTEXAI=TRUE
    GOOGLE_CLOUD_PROJECT=YOUR_GCP_PROJECT_ID
    GOOGLE_CLOUD_LOCATION=GCP_LOCATION
    MODEL=gemini-2.0-flash-001
    EOF
    ```
3.  Copy the `.env` file to the other agent directories you will use in this lab by running the following:

    ```bash
    cp langchain_tool_agent/.env crewai_tool_agent/.env
    cp langchain_tool_agent/.env function_tool_agent/.env
    cp langchain_tool_agent/.env vertexai_search_tool_agent/.env
    ```
4.  Click on the **agent.py** file in the **langchain_tool_agent** directory.
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


## Task 4. Use a CrewAI Tool
ONLY WORKS WITH OLDER 1.2.1 ADK Ver

You can similarly use [CrewAI Tools](https://github.com/crewAIInc/crewAI-tools), using a `CrewaiTool` wrapper.

1.  Using your IDE navigate to the directory **adk_tools/crewai_tool_agent**.
2.  In the **crewai_tool_agent** directory, click on the **agent.py** file.
3.  Notice the import of the `CrewaiTool` class from ADK and the `FileWriterTool` from `crewai_tools`.
4.  Add the following code where indicated in the `agent.py` file to add the [CrewAI File Write tool](https://docs.crewai.com/tools/filewritetool) to your agent, along with a name and description:

    ```python
      tools = [CrewaiTool(
        name="file_writer_tool",
        description=(
          "Writes a file to disk when run with a"
          "filename, content, overwrite set to 'true',"
          "and an optional directory"
        ),
        tool=FileWriterTool()
      )]
    ```
5.  **Save** the file.
6.  You will run this agent using the command line interface to be familiar with it as a convenient way to test an agent quickly. In the Cloud Shell Terminal, from the **adk_tools** project directory, launch the agent with the ADK command line UI with:

    ```bash
    adk run crewai_tool_agent
    ```
7.  While the agent loads, it may display some warnings. You can ignore these. When you are presented the `user:` prompt, enter:

    ```livecodeserver
    Write a poem about being part of a crew, and save it as a new file crew_poem.txt
    ```
8.  **Output:**
    ```bash
    Using Tool: File Writer Tool
    [crewai_tool_agent]: I've saved the poem to crew_poem.txt. Let me know if you need anything else. 
    ```
9.  Notice that the command line interface also indicates to you when a tool is being used.
10. In the Terminal, respond to the next `user:` prompt with `exit` **to exit the command line interface**.
11. Run the following command to print the poem from the file that the tool created:

    ```bash
    cat crew_poem.txt
    ```
12. **Example output (yours may be a little different):**
    ```bash
    United as one, we stand tall,
    A crew of dreams, ready to enthrall.
    Through stormy seas or skies so blue,
    Together we conquer, me and you.
    ```
13. Scroll back in your Terminal history to find where you ran `adk run crewai_tool_agent`, and notice that the command line interface provided you a log file to tail. Copy and run that command to view more details of the execution:

    ```bash
    tail -F /tmp/agents_log/agent.latest.log
    ```
14. Press **CTRL + C** to stop tailing the log file and return to the command prompt.

Click **Check my progress** to verify the objective.



## Task 6. Use a function as a custom tool

When pre-built tools don't fully meet specific requirements, you can create your own tools. This allows for tailored functionality, such as connecting to proprietary databases or implementing unique algorithms.

The most straightforward way to create a new tool is to write a standard Python function with a [docstring formatted properly](https://google.github.io/adk-docs/tools/function-tools/#docstring) and pass it to your model as a tool. This approach offers flexibility and quick integration.

When writing a function to be used as a tool, there are a few important things to keep in mind:

*   **Parameters:** Your function can accept any number of parameters, each of which can be of any JSON-serializable type (e.g., string, integer, list, dictionary). It's important to avoid setting default values for parameters, as the large language model (LLM) does not currently support interpreting them.
*   **Return type:** The preferred return type for a Python Function Tool is a dictionary. This allows you to structure the response with key-value pairs, providing context and clarity to the LLM. For example, instead of returning a numeric error code, return a dictionary with an `"error_message"` key containing a human-readable explanation. As a best practice, include a `"status"` key in your return dictionary to indicate the overall outcome (e.g., `"success"`, `"error"`, `"pending"`), providing the LLM with a clear signal about the operation's state.
*   **Docstring:** The docstring of your function serves as the tool's description and is sent to the LLM. Therefore, a well-written and comprehensive docstring is crucial for the LLM to understand how to use the tool effectively. Clearly explain the purpose of the function, the meaning of its parameters, and the expected return values.

Define a function and use it as a tool by completing the following steps:

1.  Using your IDE navigate to the directory **adk_tools/function_tool_agent**.
2.  In the **function_tool_agent** directory, click on the **agent.py** file.
3.  Notice that the functions `get_date()` and `write_journal_entry()` have docstrings formatted properly for an ADK agent to know when and how to use them. They include:
    *   A clear description of what each function does
    *   an `Args:` section describing the function's input parameters with JSON-serializable types
    *   a `Returns:` section describing what the function returns, with the preferred response type of a `dict`
4.  To pass the function to your agent to use as a tool, add the following code where indicated in the `agent.py` file:

    ```python
      tools=[get_date, write_journal_entry]
    ```
5.  **Save** the file.
6.  You will run this agent using the dev UI to see how its tools allow you to easily visualize tool requests and responses. In the Cloud Shell Terminal, from the **adk_tools** project directory, run the dev UI again with the following command (if the server is still running from before, stop the running server first with **CTRL+C**, then run the following to start it again):

    ```bash
    adk web
    ```
7.  Click the **http://127.0.0.1:8000** link to open the ADK Dev UI.
8.  From the **Select an agent** dropdown on the left, select the **function_tool_agent**.
9.  Start a conversation with the agent with:

    ```bash
    hello
    ```
10. The agent should prompt you about your day. **Respond with a sentence about how your day is going**, and it will write a journal entry for you.

12. Close the dev UI tab.
13. You can find your dated journal entry file in the **adk_tools** directory. 
14. To stop the server, click on the Terminal panel and press **CTRL + C**.



#### Best practices for writing functions to be used as tools include

*   **Fewer Parameters are Better:** Minimize the number of parameters to reduce complexity.
*   **Use Simple Data Types:** Favor primitive data types like `str` and `int` over custom classes when possible.
*   **Use Meaningful Names:** The function's name and parameter names significantly influence how the LLM interprets and utilizes the tool. Choose names that clearly reflect the function's purpose and the meaning of its inputs.
*   **Break Down Complex Functions:** Instead of a single `update_profile(profile: Profile)` function, create separate functions like `update_name(name: str)`, `update_age(age: int)`, etc.
*   **Return status:** Include a `"status"` key in your return dictionary to indicate the overall outcome (e.g., `"success"`, `"error"`, `"pending"`) to provide the LLM a clear signal about the operation's state.

# Deploy ADK agent to Agent Engine - Use Model Context Protocol (MCP) Tools with ADK Agents

In this lab, you will learn how to use ADK agents as MCP clients and expose tools through a custom MCP server. You will configure the server to allow standardized communication between agents and tools. This lab shows seamless integration between LLMs and external capabilities using the Model Context Protocol.




## Overview

In this lab, you will explore Model Context Protocol (MCP), an open standard that enables seamless integration between external services, data sources, tools, and applications. You will learn how to integrate MCP into your ADK agents, using tools provided by existing MCP servers to enhance your ADK workflows. Additionally, you will see how to expose ADK tools like `load_web_page` through a custom-built MCP server, enabling broader integration with MCP clients.

**What is Model Context Protocol (MCP)**

Model Context Protocol (MCP) is an open standard designed to standardize how Large Language Models (LLMs) like Gemini and Claude communicate with external applications, data sources, and tools. Think of it as a universal connection mechanism that simplifies how LLMs obtain context, execute actions, and interact with various systems.

MCP follows a client-server architecture, defining how data (resources), interactive templates (prompts), and actionable functions (tools) are exposed by an MCP server and consumed by an MCP client (which could be an LLM host application or an AI agent).

This Lab covers two primary integration patterns:

*   Using Existing MCP Servers within ADK: An ADK agent acts as an MCP client, leveraging tools provided by external MCP servers.
*   Exposing ADK Tools via an MCP Server: Building an MCP server that wraps ADK tools, making them accessible to any MCP client.

## Objectives

In this lab, you will learn how to:

*   Use an ADK agent as an MCP client to interact with tools from existing MCP servers.
*   Configure and deploy your own MCP server to expose ADK tools to other clients.
*   Connect ADK agents with external tools through standardized MCP communication.
*   Enable seamless interaction between LLMs and tools using Model Context Protocol.


## Task 2. Using Google Maps MCP server with ADK agents (ADK as an MCP client) in adk web

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
3.  Search for **Credentials** in the search bar at the top of the page. Select it from the results.
4.  On the **Credentials** page, click **+ Create Credentials** at the top of the page, then select **API key**.
    The **API key created** dialog will display your newly created API key. Be sure to save this key locally for later use in the lab.
5.  Click **Close** on the dialog box.
    Your newly created key will be named **API Key 1** by default. Select the key, rename it to **GOOGLE_MAPS_API_KEY**, and click **Save**.

### Define your Agent with an MCP Toolset for Google Maps

In this sub-section, you will configure your agent to use the `MCPToolset` for Google Maps, enabling it to seamlessly provide directions and location-based information.

1.  Using your IDE find the **adk_mcp_tools** folder. Click it to toggle it open.
2.  Navigate to the directory **adk_mcp_tools/google_maps_mcp_agent**.
3.  Paste the following command in a plain text file, then update the `YOUR_ACTUAL_API_KEY` value with the Google Maps API key you generated and saved in a previous step:

    ```bash
    cd ~/adk_mcp_tools
    cat << EOF > google_maps_mcp_agent/.env
    GOOGLE_GENAI_USE_VERTEXAI=TRUE
    GOOGLE_CLOUD_PROJECT=Project
    GOOGLE_CLOUD_LOCATION=Region
    GOOGLE_MAPS_API_KEY="YOUR_ACTUAL_API_KEY"
    EOF
    ```
4.  Copy and paste the updated command to run it and write a **.env** file which will provide authentication details for this agent directory.
5.  Copy the `.env` file to the other agent directory you will use in this lab by running the following command:

    ```bash
    cp google_maps_mcp_agent/.env adk_mcp_server/.env
    ```
6.  Click on the **agent.py** file in the **google_maps_mcp_agent** directory.
7.  Notice the import of the `MCPToolset` class from ADK, along with `StdioConnectionParams` and `StdioServerParameters`. These are used to connect to an MCP server.
8.  Add the following code where indicated in the `agent.py` file to add the Google Maps tool to your agent:

    ```python
      tools=[
        MCPToolset(
        connection_params=StdioConnectionParams(
          server_params=StdioServerParameters(
            command="python3", # Command to run your MCP server script
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
10. From the **adk_mcp_tools** project directory, **launch the Agent Development Kit Dev UI** with the following command:

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

## Task 3. Building an MCP server with ADK tools (MCP server exposing ADK)

In this section, you'll learn how to expose the ADK `load_web_page` tool through a custom-built MCP server. This pattern allows you to wrap existing ADK tools and make them accessible to any standard MCP client application.

### Create the MCP Server Script and Implement Server Logic

1.  In your IDE, find the **adk_mcp_tools** folder. Click it to toggle it open.
2.  Navigate to the directory **adk_mcp_tools/adk_mcp_server**.
3.  A Python file named **adk_server.py** has been prepared and commented for you. **Take some time to review that file**, reading the comments to understand how the code wraps a tool and serves it as an MCP server. Notice how it allows MCP clients to list available tools as well as invoke the ADK tool asynchronously, handling requests and responses in an MCP-compliant format.

### Test the Custom MCP Server with an ADK Agent

1.  Click on the **agent.py** file in the **adk_mcp_server** directory.
2.  Update the path to your **adk_server.py** file.
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
    python3 ~/adk_mcp_tools/adk_mcp_server/adk_server.py
    ```

9.  Open a Terminal and from the **adk_mcp_tools** project directory, launch the **Agent Development Kit Dev UI** with the following command:

    ```bash
    cd ~/adk_mcp_tools
    adk web
    ```
11. Click the **http://127.0.0.1:8000** link to open the ADK Dev UI.
12. From the **Select an agent** dropdown on the left, select the **adk_mcp_server** from the dropdown.
13. Query the agent with:

    ```bash
    Load the content from https://example.com.
    ```

15. What happens here:
    *   The ADK agent (`web_reader_mcp_client_agent`) uses the `MCPToolset` to connect to your `adk_server.py`.
    *   The MCP server will receive the `call_tool` request, execute the ADK `load_web_page` tool, and return the result.
    *   The ADK agent will then relay this information. You should see logs from both the ADK Web UI (and its terminal) and from your `adk_server.py` terminal in the Cloud Shell Terminal tab where it is running.
16. This demonstrates that ADK tools can be encapsulated within an MCP server, making them accessible to a broad range of MCP-compliant clients including ADK agents.


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
   adk api_server --a2a --port 8001 contributing/samples/a2a_human_in_loop/remote_a2a
   ```

2. **Run the Main Agent**:
   ```bash
   # In a separate terminal, run the adk web server
   adk web contributing/samples/
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



# Build multi-agent systems with ADK


## Objective

In this lab, you will learn about multi-agent systems using the Agent Development Kit.

After this lab, you will be able to:

*   Create multiple agents and relate them to one another with parent to sub-agent relationships
*   Build content across multiple turns of conversation and multiple agents by writing to a session's state dictionary
*   Instruct agents to read values from the session state to use as context for their responses
*   Use workflow agents to pass the conversation between agents directly




## Multi-Agent Systems

The Agent Development Kit empowers developers to get more reliable, sophisticated, multi-step behaviors from generative models. Instead of writing long, complex prompts that may not deliver results reliably, you can construct a flow of multiple, simple agents that can collaborate on complex problems by dividing tasks and responsibilities.

This architectural approach offers several key advantages such as:

*   **Easier to design:** You can think in terms of agents with specific jobs and skills.
*   **Specialized functions with more reliable performance:** Specialized agents can learn from clear examples to become more reliable at their specific tasks.
*   **Organization:** Dividing the workflow into distinct agents allows for a more organized, and therefor easier to think about, approach.
*   **Improvability and maintainability:** It is easier to improve or fix a specialized component rather than make changes to a complex agent that may fix one behavior but might impact others.
*   **Modularity:** Distinct agents from one workflow can be easily copied and included in other similar workflows.

## The Hierarchical Agent Tree

In Agent Development Kit, you organize your agents in a tree-like structure. This helps limit the options for transfers for each agent in the tree, making it easier to control and predict the possible routes the conversation can take through the tree. Benefits of the hierarchical structure include:

*   It draws **inspiration from real-world collaborative teams**, making it easier to design and reason about the behavior of the multi-agent system.
*   It is **intuitive for developers**, as it mirrors common software development patterns.
*   It provides **greater control over the flow** of information and task delegation within the system, making it easier to understand possible pathways and debug the system. For example, if a system has two report-generation agents at different parts of its flow with similar descriptions, the tree structure makes it easier to ensure that the correct one is invoked.

The structure always begins with the agent defined in the **root_agent** variable (although it may have a different user-facing **name** to identify itself). The `root_agent` may act as a **parent** to one or more **sub-agents**. Each sub-agent agent may have its own sub-agents.




## Task 2. Explore transfers between parent, sub-agent, and peer agents

The conversation always begins with the agent defined as the **root_agent** variable.

The default behavior of a parent agent is to understand the **description** of each sub-agent and determine if control of the conversation should be transferred to a sub-agent at any point.

You can help guide those transfers in the parent's `instruction` by referring to the sub-agents by name (the values of their `name` parameter, not their variable names). Try an example:

1.  In the Cloud Shell Terminal, run the following to create a `.env` file to authenticate the agent in the **parent_and_subagents** directory.

    ```bash
    cd ~/adk_multiagent_systems
    cat << EOF > parent_and_subagents/.env
    GOOGLE_GENAI_USE_VERTEXAI=TRUE
    GOOGLE_CLOUD_PROJECT={{{project_0.project_id| YOUR_GCP_PROJECT_ID}}}
    GOOGLE_CLOUD_LOCATION={{{project_0.default_region| GCP_LOCATION}}}
    MODEL=gemini-2.5-flash
    EOF
    ```
2.  Run the following command to copy that `.env` file to the **workflow_agents** directory, which you will use later in the lab:

    ```bash
    cp parent_and_subagents/.env workflow_agents/.env
    ```
3.  In the Cloud Shell Editor file explorer pane, navigate to the **adk_multiagent_systems/parent_and_subagents** directory.
4.  Click on the **agent.py** file to open it.

5.  Notice that there are three agents here:
    *   a **root_agent** named `steering` (its name is used to identify it in ADK's dev UI and command line interfaces). It asks the user a question (if they know where they'd like to travel or if they need some help deciding), and the user's response to that question will help this steering agent know which of its two sub-agents to steer the conversation towards. Notice that it only has a simple `instruction` that does not mention the sub-agents, but it is aware of its sub-agents' descriptions.
    *   a **travel_brainstormer** that helps the user brainstorm destinations if they don't know where they would like to visit.
    *   an **attractions_planner** that helps the user build a list of things to do once they know which country they would like to visit.
6.  Make **travel_brainstormer** and **attractions_planner** sub-agents of the **root_agent** by adding the following line to the creation of the **root_agent**:

    ```ini
        sub_agents=[travel_brainstormer, attractions_planner]
    ```
7.  **Save** the file.
8.  Note that you don't add a corresponding *parent* parameter to the sub-agents. The hierarchical tree is defined only by specifying `sub_agents` when creating parent agents.
9.  In the Cloud Shell Terminal, run the following to use the ADK command line interface to chat with your agent:

    ```bash
    cd ~/adk_multiagent_systems
    adk run parent_and_subagents
    ```
10. When you are presented the `[user]:` prompt, greet the agent with:

    ```bash
    hello
    ```

    **Example output (yours may be a little different):**

    ```
    user: hello
    [steering]: Hi there! Do you already have a country in mind for your trip, or would you like some help deciding where to go?
    ```
11. Tell the agent:

    ```bash
    I could use some help deciding.
    ```

    **Example output (yours may be a little different):**

    ```
    user: I could use some help deciding.
    [travel_brainstormer]: Okay! To give you the best recommendations, I need to understand what you're looking for in a trip.
    ...
    ```
12. Notice from the name **[travel_brainstormer]** in brackets in the response that the **root_agent** (named **[steering]**) has transferred the conversation to the appropriate sub-agent based on that sub-agent's `description` alone.
13. At the `user:` prompt, enter `exit` to end the conversation.
14. You can also provide your agent more detailed instructions about when to transfer to a sub-agent as part of its `instructions`. In the **agent.py** file, add the following lines to the **root_agent**'s `instruction`:

    ```vhdl
        If they need help deciding, send them to
        'travel_brainstormer'.
        If they know what country they'd like to visit,
        send them to the 'attractions_planner'.
    ```
15. **Save** the file.
16. In the Cloud Shell Terminal, run the following to start the command line interface again:

    ```bash
    adk run parent_and_subagents
    ```
17. Greet the agent with:

    ```bash
    hello
    ```
18. Reply to the agent with:

    ```vhdl
    Actually I don't know what country to visit.
    ```

    **Example output (yours may be a little different):**

    ```
    user: actually I don't know what country to visit
    [travel_brainstormer]: Okay! I can help you brainstorm some countries for travel...
    ```
19. Notice you have been transferred to the **travel_brainstormer** agent, which is a **peer** agent to the **attractions_planner**. This is allowed by default. If you wanted to prevent transfers to peers, you could have set the `disallow_transfer_to_peers` parameter to `True` on the **attractions_planner** agent.
20. At the user prompt, type `exit` to end the session.

    #### Step-by-step pattern
    If you are interested in an agent that guides a user through a process step-by-step, one useful pattern can be to make the first step the `root_agent` with the second step agent its only sub-agent, and continue with each additional step being the only sub-agent of the previous step's agent.
21. Click **Check my progress** to verify the objective.

## Task 3. Use session state to store and retrieve specific information

Each conversation in ADK is contained within a `Session` that all agents involved in the conversation can access. A session includes the conversation history, which agents read as part of the context used to generate a response. The session also includes a **session state** dictionary that you can use to take greater control over the most important pieces of information you would like to highlight and how they are accessed.

This can be particularly helpful to pass information between agents or to maintain a simple data structure, like a list of tasks, over the course of a conversation with a user.

To explore adding to and reading from state:

1.  Return to the file **adk_multiagent_systems/parent_and_subagents/agent.py**
2.  Paste the following function definition after the `# Tools` header:

    ```python
    def save_attractions_to_state(
        tool_context: ToolContext,
        attractions: List[str]
    ) -> dict[str, str]:
        """Saves the list of attractions to state["attractions"].

        Args:
            attractions [str]: a list of strings to add to the list of attractions

        Returns:
            None
        """
        # Load existing attractions from state. If none exist, start an empty list
        existing_attractions = tool_context.state.get("attractions", [])

        # Update the 'attractions' key with a combo of old and new lists.
        # When the tool is run, ADK will create an event and make
        # corresponding updates in the session's state.
        tool_context.state["attractions"] = existing_attractions + attractions

        # A best practice for tools is to return a status message in a return dict
        return {"status": "success"}
    ```
3.  In this code, notice:
    *   The session is passed to your tool function as `ToolContext`. All you need to do is assign a parameter to receive it, as you see here with the parameter named `tool_context`. You can then use `tool_context` to access session information like conversation history (through `tool_context.events`) and the session state dictionary (through `tool_context.state`). When the `tool_context.state` dictionary is modified by your tool function, those changes will be reflected in the session's state after the tool finishes its execution.
    *   The docstring provides a clear description and sections for argument and return values.
    *   The commented function code demonstrates how easy it is to make updates to the state dictionary.
4.  Add the tool to the **attractions_planner** agent by adding the `tools` parameter when the agent is created:

    ```ini
        tools=[save_attractions_to_state]
    ```
5.  Add the following bullet points to the **attractions_planner** agent's existing `instruction` parameter:

    ```stata
        - When they reply, use your tool to save their selected attraction
        and then provide more possible attractions.
        - If they ask to view the list, provide a bulleted list of
        {{ attractions? }} and then suggest some more.
    ```
6.  Notice how state is provided to the instructions by using dynamic templating: `{{ attractions? }}`. This loads the value of the `attractions` field, and the question mark prevents this from erroring if the field is not yet present.
7.  You will now run the agent from the web interface, which provides a tab for you to see the changes being made to the session state. **Launch the Agent Development Kit Web UI** with the following command:

    ```ebnf
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
8.  To view the web interface in a new tab, click the **http://127.0.0.1:8000** link in the Terminal output.
9.  A new browser tab will open with the ADK Dev UI.
10. From the **Select an agent** dropdown on the left, select the **parent_and_subagents** agent from the dropdown.
11. Start the conversation with: `hello`
12. After the agent greets you, reply with `I'd like to go to Egypt.` You should be transferred to the **attractions_planner** and be provided a list of attractions.
13. Choose an attraction, for example:

    ```vhdl
    I'll go to the Sphinx
    ```
14. You should receive an acknowledgement in the response, like: *Okay, I've saved The Sphinx to your list. Here are some other attractions...*
15. Click the response tool box (marked with a check mark) to view the event created from the tool's response. Notice that it includes an **actions** field which includes **state_delta** describing the changes to the state.
16. You should be prompted by the agent to select more attractions. Reply to the agent by **naming one of the options it has presented**.
17. On the left-hand navigation menu, click the "X" to exit the focus on the event you inspected earlier.
18. Now in the sidebar, you should see the list of events and a few tab options. Select the **State** tab. Here you can view the current state, including your **attractions** array with the two values you have requested.

    [Image of Session State preview in the Web UI]
19. Send this message to the agent: `What is on my list?`
20. It should return your list formatted as a bulleted list according to its `instruction`.
21. When you are finished experimenting with the agent, close the web browser tab and press **CTRL + C** in the Cloud Shell Terminal to stop the server.

    **Note:** Instead of saving small pieces of information, if you would like to store your agent's entire text response in the state dictionary, you can set an `output_key` parameter when you define the agent, and its entire output will be stored in the state dictionary under that field name.
22. Click **Check my progress** to verify the objective.

## Workflow Agents

Parent to sub-agent transfers are ideal when you have multiple specialist sub-agents, and you want the user to interact with each of them.

However, if you would like agents to act one-after-another without waiting for a turn from the user, you can use **workflow agents**. Some example scenarios when you might use workflow agents include when you would like your agents to:

*   **Plan and Execute:** When you want to have one agent prepare a list of items, and then have other agents use that list to perform follow-up tasks, for example writing sections of a document
*   **Research and Write:** When you want to have one agent call functions to collect contextual information from Google Search or other data sources, then another agent use that information to produce some output.
*   **Draft and Revise:** When you want to have one agent prepare a draft of a document, and then have other agents check the work and iterate on it

To accomplish these kinds of tasks, **workflow agents** have sub-agents and guarantee that each of their sub-agents acts. Agent Development Kit provides three built-in workflow agents and the opportunity to define your own:

*   `SequentialAgent`
*   `LoopAgent`
*   `ParallelAgent`

Throughout the rest of this lab, you will build a multi-agent system that uses multiple LLM agents, workflow agents, and tools to help control the flow of the agent.

In particular, you will build an agent that will develop a pitch document for a new hit movie: a biographical film based on the life of a historical character. Your sub-agents will handle the research, an iterative writing loop with a screenwriter and a critic, and finally some additional sub-agents will help brainstorm casting ideas and use historical box office data to make some predictions about box office results.

In the end, your multi-agent system will look like this (you can click on the image to see it larger):

[Image of Film_concept_team multi-agent system step 2]

But you will begin with a simpler version.

## Task 4. Begin building a multi-agent system with a SequentialAgent

The `SequentialAgent` executes its sub-agents in a linear sequence. Each sub-agent in its `sub_agents` list is run, one after the other, in the order they are defined.

This is ideal for workflows where tasks must be performed in a specific order, and the output of one task serves as the input for the next.

In this task, you will run a `SequentialAgent` to build a first version of your movie pitch-development multi-agent system. The first draft of your agent will be structured like this:

[Image of Film_concept_team multi-agent system step 1]

*   A **root_agent** named **greeter** to welcome the user and request a historical character as a movie subject
*   A `SequentialAgent` called **film_concept_team** will include:
    *   A **researcher** to learn more about the requested historical figure from Wikipedia, using a LangChain tool covered in the lab *Empower ADK agents with tools*. An agent can choose to call its tool(s) multiple times in succession, so the researcher can take multiple turns in a row if it determines it needs to do more research.
    *   A **screenwriter** to turn the research into a plot outline.
    *   A **file_writer** to title the resulting movie and write the results of the sequence to a file.

1.  In the **Cloud Shell Editor**, navigate to the directory **adk_multiagent_systems/workflow_agents**.
2.  Click on the **agent.py** file in the **workflow_agents** directory.
3.  Read through this agent definition file. Because sub-agents must be defined before they can be assigned to a parent, to read the file in the order of the conversation flow, you can read the agents from the bottom of the file to the top.
4.  You also have a function tool **append_to_state**. This function allows agents with the tool the ability to add content to a dictionary value in state. It is particularly useful for agents that might call a tool multiple times or act in multiple passes of a `LoopAgent`, so that each time they act their output is stored.
5.  Try out the current version of the agent by launching the web interface from the Cloud Shell Terminal with:

    ```bash
    cd ~/adk_multiagent_systems
    adk web
    ```

    **Note:** If you did not shut down your previous `adk web` session, the default port of 8000 will be blocked, but you can launch the Dev UI with a new port by using `adk web --port 8001`, for example.
6.  To view the web interface in a new tab, click the **http://127.0.0.1:8000** link in the Terminal output.
7.  A new browser tab will open with the ADK Dev UI.
8.  From the **Select an agent** dropdown on the left, select **workflow_agents**.
9.  Begin the conversation with: `hello`. It may take a few moments for the agent to respond, but it should request you enter a historical figure to start your film plot generation.
10. When prompted to enter a historical figure, you can enter one of your choice or use one of these examples:
    *   `Zhang Zhongjing` - a renowned Chinese physician from the 2nd Century CE.
    *   `Ada Lovelace` - an English mathematician and writer known for her work on early computers
    *   `Marcus Aurelius` - a Roman emperor known for his philosophical writings.
11. Once you have chosen a type of character, the agent should work its way through the sequence and finally give the film a title and write the plot outline file to your **~/adk_multiagent_systems/movie_pitches** directory. It should inform you when it has written the file to disk.
    If you don't see the agent reporting that it generated a file for you or want to try another character, you can click **+ New Session** in the upper right and try again.
12. View the agent's output in the Cloud Shell Editor. (You may need to use the Cloud Shell Editor's menu to enable View > Word Wrap to see the full text without lots of horizontal scrolling.)
13. In the ADK Dev UI, **click on one of the agent icons** ([Image of agent_icon]) representing a turn of conversation to bring up the **event view**.
14. The event view provides a visual representation of the tree of agents and tools used in this session. You may need to scroll in the event panel to see the full plot.
15. In addition to the graph view, you can click on the **Request** tab of the event to see the information this agent received as part of its request, including the conversation history.
16. You can also click on the **Response** tab of the event to see what the agent returned.
17. When you are finished inspecting the events, close the browser tab and press **CTRL+C** in the Cloud Shell Terminal to stop the server.

18. Click **Check my progress** to verify the objective.

## Task 5. Add a LoopAgent for iterative work

The `LoopAgent` executes its sub-agents in a defined sequence and then starts at the beginning of the sequence again without breaking for a user input. It repeats the loop until a number of iterations has been reached or a call to exit the loop has been made by one of its sub-agents (usually by calling a built-in `exit_loop` tool).

This is beneficial for tasks that require continuous refinement, monitoring, or cyclical workflows. Examples include:

*   **Iterative Refinement:** Continuously improve a document or plan through repeated agent cycles.
*   **Continuous Monitoring:** Periodically check data sources or conditions using a sequence of agents.
*   **Debate or Negotiation:** Simulate iterative discussions between agents to reach a better outcome.

You will add a `LoopAgent` to your movie pitch agent to allow multiple rounds of research and iteration while crafting the story. In addition to refining the script, this allows a user to start with a less specific input: instead of suggesting a specific historical figure, they might only know they want a story about an ancient doctor, and a research-and-writing iteration loop will allow the agents to find a good candidate, then work on the story.

[Image of Film_concept_team multi-agent system step 2]

Your revised agent will flow like this:

*   The **root_agent** `greeter` will remain the same.
*   The **film_concept_team** `SequentialAgent` will now consist of:
    *   A **writers_room** `LoopAgent` that will begin the sequence. It will consist of:
        *   The **researcher** will be the same as before.
        *   The **screenwriter** will be similar to before.
        *   A **critic** that will offer critical feedback on the current draft to motivate the next round of research and improvement through the loop.
*   When the loop terminates, it will escalate control of the conversation back to the **film_concept_team** `SequentialAgent`, which will then pass control to the next agent in its sequence: the **file_writer** that will remain as before to give the movie a title and write the results of the sequence to a file.

To make these changes:

1.  In the **adk_multiagent_systems/workflow_agents/agent.py** file, paste the following new agent into the **agent.py** file under the **# Agents** section header (without overwriting the existing agents):

    ```smalltalk
    critic = Agent(
      name="critic",
      model=model_name,
      description="Reviews the outline so that it can be improved.",
      instruction="""
      INSTRUCTIONS:
      Consider these questions about the PLOT_OUTLINE:
      - Does it meet a satisfying three-act cinematic structure?
      - Do the characters' struggles seem engaging?
      - Does it feel grounded in a real time period in history?
      - Does it sufficiently incorporate historical details from the RESEARCH?

      If significant improvements can be made, use the 'append_to_state' tool to add your feedback to the field 'CRITICAL_FEEDBACK'.
      Explain your decision and briefly summarize the feedback you have provided.

      PLOT_OUTLINE:
      {{ PLOT_OUTLINE? }}

      RESEARCH:
      {{ research? }}
      """,
      before_model_callback=log_query_to_model,
      after_model_callback=log_model_response,
      tools=[append_to_state],
    )
    ```
2.  Create a new `LoopAgent` called **writers_room** that creates the iterative loop of the researcher, screenwriter, and critic. Each pass through the loop will end with a critical review of the work so far, which will prompt improvements for the next round. Paste the following above the existing **film_concept_team** `SequentialAgent`.

    ```routeros
    writers_room = LoopAgent(
      name="writers_room",
      description="Iterates through research and writing to improve a movie plot outline.",
      sub_agents=[
        researcher,
        screenwriter,
        critic
      ],
      max_iterations=5,
    )
    ```
3.  Note that the `LoopAgent` creation includes a parameter for `max_iterations`. This defines how many times the loop will run before it ends. Even if you plan to interrupt the loop via another method, it is a good idea to include a cap on the total number of iterations.
4.  You can also use a tool to exit the loop upon a specific condition. Add the following to your imports at the top of the **adk_multiagent_systems/workflow_agents/agent.py**:

    ```moonscript
    from google.adk.tools import exit_loop
    ```
5.  Provide the tool to the **critic** agent by updating its `tools` parameter to include this tool:

    ```ini
        tools=[append_to_state, exit_loop],
    ```
6.  Add the following to the **critic**'s `instruction` parameter, after its bulleted list of questions:

    ```awk
        If the PLOT_OUTLINE does a good job with these questions, exit the writing loop with your 'exit_loop' tool.
    ```
7.  Update the existing **film_concept_team** agent's **sub_agents** list to include the `preproduction_team` between the **writers_room** and **file_writer**:

    ```routeros
    film_concept_team = SequentialAgent(
      name="film_concept_team",
      description="Write a film plot outline and save it as a text file.",
      sub_agents=[
        writers_room,
        preproduction_team,
        file_writer
      ],
    )
    ```
8.  **Save** the file.
9.  Launch the web interface from the Cloud Shell Terminal with the following command (remember, if your server is already running, close it by selecting the Cloud Shell Terminal where it is running and pressing **CTRL+C** before you can restart the server):

    ```bash
    cd ~/adk_multiagent_systems
    adk web
    ```
10. To view the web interface in a new tab, click the **http://127.0.0.1:8000** link in the Terminal output.
11. A new browser tab will open with the ADK Dev UI.
12. From the **Select an agent** dropdown on the left, select **workflow_agents**.
13. Begin a new conversation with: `hello`.
14. When prompted to choose a kind of historical character, choose one that interests you. Some ideas include:
    *   `an industrial designer who made products for the masses`
    *   `a cartographer (a map maker)`
    *   `that guy who made crops yield more food`
15. Once you have chosen a type of character, the agent should work its way through iterations of the loop and finally give the film a title and write the outline to a file.
16. Using the Cloud Shell Editor, review the file generated, which should be saved in the **adk_multiagent_systems/movie_pitches** directory. If a part of the process fails, **start a new session** and try again.

17. Click **Check my progress** to verify the objective.

## Task 6. Use a "fan out and gather" pattern for report generation with a ParallelAgent

The `ParallelAgent` enables concurrent execution of its sub-agents. Each sub-agent operates in its own branch, and by default, they do not share conversation history or state directly with each other during parallel execution.

This is valuable for tasks that can be divided into independent sub-tasks that can be processed simultaneously. Using a `ParallelAgent` can significantly reduce the overall execution time for such tasks.

In this lab, you will add some supplemental reports -- some research on potential box office performance and some initial ideas on casting -- to enhance the pitch for your new film.

[Image of Film_concept_team multi-agent system step 3]

Your revised agent will flow like this:

*   The **greeter** will the same.
*   The **film_concept_team** `SequentialAgent` will now consist of:
    *   The **writers_room** `LoopAgent`, which will remain the same including:
        *   The **researcher** agent
        *   The **screenwriter** agent
        *   The **critic** agent
    *   Your new **preproduction_team** `ParallelAgent` will then act, consisting of:
        *   A **box_office_researcher** agent to use historical box office data to generate a report on potential box office performance for this film
        *   A **casting_agent** agent to generate some initial ideas on casting based on actors who have starred in similar films
    *   The **file_writer** that will remain as before to write the results of the sequence to a file.

While much of this example demonstrates creative work that would be done by human teams, this workflow represents how a complex chain of tasks can be broken across several sub-agents to produce drafts of complex documents which human team members can then edit and improve upon.

1.  Paste the following new agents and `ParallelAgent` into your **workflow_agents/agent.py** file under the `# Agents` header:

    ```routeros
    box_office_researcher = Agent(
      name="box_office_researcher",
      model=model_name,
      description="Considers the box office potential of this film",
      instruction="""
      PLOT_OUTLINE:
      {{ PLOT_OUTLINE? }}

      INSTRUCTIONS:
      Write a report on the box office potential of a movie like that described in PLOT_OUTLINE based on the reported box office performance of other recent films.
      """,
      output_key="box_office_report"
    )

    casting_agent = Agent(
      name="casting_agent",
      model=model_name,
      description="Generates casting ideas for this film",
      instruction="""
      PLOT_OUTLINE:
      {{ PLOT_OUTLINE? }}

      INSTRUCTIONS:
      Generate ideas for casting for the characters described in PLOT_OUTLINE
      by suggesting actors who have received positive feedback from critics and/or
      fans when they have played similar roles.
      """,
      output_key="casting_report"
    )

    preproduction_team = ParallelAgent(
      name="preproduction_team",
      sub_agents=[
        box_office_researcher,
        casting_agent
      ]
    )
    ```
2.  Update the existing **film_concept_team** agent's **sub_agents** list to include the `preproduction_team` between the **writers_room** and **file_writer**:

    ```routeros
    film_concept_team = SequentialAgent(
      name="film_concept_team",
      description="Write a film plot outline and save it as a text file.",
      sub_agents=[
        writers_room,
        preproduction_team,
        file_writer
      ],
    )
    ```
3.  **Save** the file.
4.  Update the **file_writer**'s **instruction** to:

    ```n1ql
      INSTRUCTIONS:
      - Create a marketable, contemporary movie title suggestion for the movie described in the PLOT_OUTLINE. If a title has been suggested in PLOT_OUTLINE, you can use it, or replace it with a better one.
      - Use your 'write_file' tool to create a new txt file with the following arguments:
        - for a filename, use the movie title
        - Write to the 'movie_pitches' directory.
        - For the 'content' to write, include:
          - The PLOT_OUTLINE
          - The BOX_OFFICE_REPORT
          - The CASTING_REPORT

      PLOT_OUTLINE:
      {{ PLOT_OUTLINE? }}

      BOX_OFFICE_REPORT:
      {{ box_office_report? }}

      CASTING_REPORT:
      {{ casting_report? }}
    ```
5.  **Save** the file.
6.  In the Terminal, stop the server with **CTRL+C** and then run it again with `adk web`.
7.  Click on the link in the Terminal output to return to the ADK Dev UI browser tab, and select **workflow_agents** from the dropdown.
8.  Enter `hello` to begin a new conversation.
9.  When prompted, enter a new character idea that you are interested in. Some ideas include:
    *   `that actress who invented the technology for wifi`
    *   `an exciting chef`
    *   `key players in the worlds fair exhibitions`
10. When the agent has completed its writing and report-generation, inspect the file it produced in the **adk_multiagent_systems/movie_pitches** directory. If a part of the process fails, **start a new session** and try again.

17. Click **Check my progress** to verify the objective.

## Custom workflow agents

When the pre-defined workflow agents of `SequentialAgent`, `LoopAgent`, and `ParallelAgent` are insufficient for your needs, `CustomAgent` provides the flexibility to implement new workflow logic. You can define patterns for flow control, conditional execution, or state management between sub-agents. This is useful for complex workflows, stateful orchestrations, or integrating custom business logic into the framework's orchestration layer.

Creation of a `CustomAgent` is out of the scope of this lab, but it is good to know that it exists if you need it!

## Congratulations!

In this lab, you’ve learned to:

*   Create multiple agents and relate them to one another with parent to sub-agent relationships
*   Add to the session state and read it in agent instructions
*   Use workflow agents to pass the conversation between agents directly

## Next Steps

Learn to deploy agents to Agent Engine in the lab *Deploy ADK agents to Agent Engine*.

### Google Cloud training and certification

...helps you make the most of Google Cloud technologies. [Our classes](https://cloud.google.com/training) include technical skills and best practices to help you get up to speed quickly and continue your learning journey. We offer fundamental to advanced level training, with on-demand, live, and virtual options to suit your busy schedule. [Certifications](https://cloud.google.com/certification/) help you validate and prove your skill and expertise in Google Cloud technologies.

**Manual Last Updated May 22, 2025**

**Lab Last Tested May 22, 2025**

Copyright 2023 Google LLC All rights reserved. Google and the Google logo are trademarks of Google LLC. All other company and product names may be trademarks of the respective companies with which they are associated.
```




## Task 6. Preview a multi-agent example

You will learn more about building multi-agent systems in the lab *Build multi-agent systems with ADK*, but because multi-agent capabilities are core to the Agent Development Kit experience, you can explore one multi-agent system now.

This agentic system evaluates and improves the factual grounding of responses generated by LLMs. It includes:
- a `critic_agent` to serve as an automated fact-checker
- a `reviser_agent` to rewrite responses if needed to correct inaccuracies based on verified findings

To explore this agent:

1.  To explore this multi-agent system's code, use the Cloud Shell Editor file explorer to navigate to the directory **adk_project/llm_auditor**.
2.  Within the **llm_auditor** directory, select the **agent.py** file.
3.  Here are a few things to notice about this multi-agent example:
    *   Notice the import and use of the `SequentialAgent` class. This is an example of a **workflow class** which passes control of the conversation from one agent to the next in order without awaiting a user turn in-between. When you run the agent, you will see responses from both the `critic_agent` and the `reviser_agent`, in that order, without waiting for a user turn.
    *   Notice that these sub-agents are each imported from their own directories within a `sub_agents` directory.
    *   In the sub-agents' directories, you will see the `__init__.py` and `agent.py` files like those you explored in the directory structure earlier, along with a `prompt.py` file, which provides a dedicated place for a complete, well-structured prompt to be stored and edited before it is imported into the `agent.py` file.
4.  Create a .env file for this agent and launch the dev UI again by running the following in the Cloud Shell Terminal:

    ```bash
    cd ~/adk_project
    cat << EOF > llm_auditor/.env
    GOOGLE_GENAI_USE_VERTEXAI=TRUE
    GOOGLE_CLOUD_PROJECT=qwiklabs-gcp-00-97660de20650
    GOOGLE_CLOUD_LOCATION=us-central1
    MODEL=gemini-2.0-flash-001
    EOF

    adk web
    ```
    > **Note:** If you did not shut down your previous `adk web` session, the default port of 8000 will be blocked, but you can launch the Dev UI with a new port by using `adk web --port 8001`, for example.
5.  Click the **http://127.0.0.1:8000** link in the Terminal output. A new browser tab will open with the ADK Dev UI.
6.  From the **Select an agent** dropdown on the left, select **llm_auditor**.
7.  Start the conversation with the following false statement:

    ```smali
    Double check this: Earth is further away from the Sun than Mars.
    ```
8.  You should see two responses from the agent in the chat area:
    *   First, a detailed response from the `critic_agent` checking the truthfulness of the statement based on fact-checking with Google Search.
    *   Second, a short revised statement from the `reviser_agent` with a corrected version of your false input statement, for example, "Earth is closer to the Sun than Mars."
9.  Next to each response, click on the agent icon (![agent_icon](https://www.cloudskillsboost.google/focuses/126142?catalog_rank=%7B%22rank%22%3A3%2C%22num_filters%22%3A0%2C%22has_search%22%3Atrue%7D&parent=catalog&search_id=49852970#step11)) to open the event panel for that response (or find the corresponding numbered event on the Events panel and select it). At the top of the event view, there is a graph that visualizes the relationships between the agents and tools in this multi-agent system. The agent responsible for this response will be highlighted.
10. Feel free to explore the code further or ask for other fact-checking examples in the dev UI. Another example you can try is:

    ```livecodeserver
    Q: Why is the sky blue? A: Because the sky reflects the color of the ocean.
    ```
11. If you would like to reset the conversation, use the **+ New Session** link at the top right of the ADK Dev UI to restart the conversation.
12. When you are finished asking questions of this agent, close the browser tab and press **CTRL + C** in the Terminal to stop the server.

Click **Check my progress** to verify the objective.

#### Human-in-the-loop pattern

Even though this example uses a `SequentialAgent` workflow agent, you can think of this pattern as a human-in-the-loop pattern. When the `SequentialAgent` ends its sequence, the conversation goes back to its parent, the `llm_auditor` in this example, to get a new input turn from the user and then pass the conversation back around to the other agents.
