
# DRAFT WIP

## Task 3. Run an agent programmatically (SKIP)

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


