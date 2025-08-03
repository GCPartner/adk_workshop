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




## Task 1. Explore transfers between parent, sub-agent, and peer agents

The conversation always begins with the agent defined as the **root_agent** variable.

The default behavior of a parent agent is to understand the **description** of each sub-agent and determine if control of the conversation should be transferred to a sub-agent at any point.

You can help guide those transfers in the parent's `instruction` by referring to the sub-agents by name (the values of their `name` parameter, not their variable names). Try an example:


1.  In the Cloud Shell Editor file explorer pane, navigate to the **adk_multiagent_systems/parent_and_subagents** directory.
2.  Click on the **agent.py** file to open it.

3.  Notice that there are three agents here:
    *   a **root_agent** named `steering` (its name is used to identify it in ADK's dev UI and command line interfaces). It asks the user a question (if they know where they'd like to travel or if they need some help deciding), and the user's response to that question will help this steering agent know which of its two sub-agents to steer the conversation towards. Notice that it only has a simple `instruction` that does not mention the sub-agents, but it is aware of its sub-agents' descriptions.
    *   a **travel_brainstormer** that helps the user brainstorm destinations if they don't know where they would like to visit.
    *   an **attractions_planner** that helps the user build a list of things to do once they know which country they would like to visit.
6.  Make **travel_brainstormer** and **attractions_planner** sub-agents of the **root_agent** by adding the following line to the creation of the **root_agent**:

    ```ini
    sub_agents=[travel_brainstormer, attractions_planner]
    ```
7.  **Save** the file.
8.  Note that you don't add a corresponding *parent* parameter to the sub-agents. The hierarchical tree is defined only by specifying `sub_agents` when creating parent agents.
9.  Run the following to use the ADK command line interface to chat with your agent:

    ```bash
    cd ~/adk_workshop/adk_multiagent_systems
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
    I would like to go to Japan.
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
19. Send this message to the agent: `What is on my list?`
20. It should return your list formatted as a bulleted list according to its `instruction`.
21. When you are finished experimenting with the agent, close the web browser tab and press **CTRL + C** in the Cloud Shell Terminal to stop the server.

    **Note:** Instead of saving small pieces of information, if you would like to store your agent's entire text response in the state dictionary, you can set an `output_key` parameter when you define the agent, and its entire output will be stored in the state dictionary under that field name.

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

Lets begin with a simple version.

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

1.  Using your IDE, navigate to the directory **adk_multiagent_systems/workflow_agents**.
2.  Click on the **agent.py** file in the **workflow_agents** directory.
3.  Read through this agent definition file. Because sub-agents must be defined before they can be assigned to a parent, to read the file in the order of the conversation flow, you can read the agents from the bottom of the file to the top.
4.  You also have a function tool **append_to_state**. This function allows agents with the tool the ability to add content to a dictionary value in state. It is particularly useful for agents that might call a tool multiple times or act in multiple passes of a `LoopAgent`, so that each time they act their output is stored.
5.  Try out the current version of the agent by launching the web interface:

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
    *   `Mike Tyson` - a renowned Chinese physician from the 2nd Century CE.
    *   `Ada Lovelace` - an English mathematician and writer known for her work on early computers
    *   `Marcus Aurelius` - a Roman emperor known for his philosophical writings.
11. Once you have chosen a type of character, the agent should work its way through the sequence and finally give the film a title and write the plot outline file to your **~/adk_multiagent_systems/movie_pitches** directory. It should inform you when it has written the file to disk.
    If you don't see the agent reporting that it generated a file for you or want to try another character, you can click **+ New Session** in the upper right and try again.
13. In the ADK Dev UI, **click on one of the agent icons** representing a turn of conversation to bring up the **event view**.
14. The event view provides a visual representation of the tree of agents and tools used in this session. You may need to scroll in the event panel to see the full plot.
15. In addition to the graph view, you can click on the **Request** tab of the event to see the information this agent received as part of its request, including the conversation history.
16. You can also click on the **Response** tab of the event to see what the agent returned.
17. When you are finished inspecting the events, close the browser tab and press **CTRL+C** in the Cloud Shell Terminal to stop the server.


## Task 5. Add a LoopAgent for iterative work

The `LoopAgent` executes its sub-agents in a defined sequence and then starts at the beginning of the sequence again without breaking for a user input. It repeats the loop until a number of iterations has been reached or a call to exit the loop has been made by one of its sub-agents (usually by calling a built-in `exit_loop` tool).

This is beneficial for tasks that require continuous refinement, monitoring, or cyclical workflows. Examples include:

*   **Iterative Refinement:** Continuously improve a document or plan through repeated agent cycles.
*   **Continuous Monitoring:** Periodically check data sources or conditions using a sequence of agents.
*   **Debate or Negotiation:** Simulate iterative discussions between agents to reach a better outcome.

You will add a `LoopAgent` to your movie pitch agent to allow multiple rounds of research and iteration while crafting the story. In addition to refining the script, this allows a user to start with a less specific input: instead of suggesting a specific historical figure, they might only know they want a story about an ancient doctor, and a research-and-writing iteration loop will allow the agents to find a good candidate, then work on the story.

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
7.  Update the existing **film_concept_team** `SequentialAgent` to replace the **researcher** and **screenwriter** with the **writers_room** `LoopAgent` you just created. The **file_writer** agent should remain at the end of the sequence. The **film_concept_team** should now look like this:



    ```
    film_concept_team = SequentialAgent(
        name="film_concept_team",
        description="Write a film plot outline and save it as a text file.",
        sub_agents=[
            writers_room,
            file_writer
        ],
    )
    ```
8.  **Save** the file.
9.  Launch the web interface:

    ```bash
    cd ~adk_workshop/adk_multiagent_systems
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
16. Review the file generated, which should be saved in the **adk_multiagent_systems/movie_pitches** directory. If a part of the process fails, **start a new session** and try again.

## Task 6. Use a "fan out and gather" pattern for report generation with a ParallelAgent

The `ParallelAgent` enables concurrent execution of its sub-agents. Each sub-agent operates in its own branch, and by default, they do not share conversation history or state directly with each other during parallel execution.

This is valuable for tasks that can be divided into independent sub-tasks that can be processed simultaneously. Using a `ParallelAgent` can significantly reduce the overall execution time for such tasks.

In this lab, you will add some supplemental reports -- some research on potential box office performance and some initial ideas on casting -- to enhance the pitch for your new film.

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


## Custom workflow agents

When the pre-defined workflow agents of `SequentialAgent`, `LoopAgent`, and `ParallelAgent` are insufficient for your needs, `CustomAgent` provides the flexibility to implement new workflow logic. You can define patterns for flow control, conditional execution, or state management between sub-agents. This is useful for complex workflows, stateful orchestrations, or integrating custom business logic into the framework's orchestration layer.

Creation of a `CustomAgent` is out of the scope of this lab, but it is good to know that it exists if you need it!







