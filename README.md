# Agent Development Kit (ADK) Workshop

## Introduction
The [**Agent Development Kit (ADK)**](https://google.github.io/adk-docs/) is a powerful framework for building, testing, and deploying intelligent agentic applications. This workshop will guide you through the core concepts of ADK, from creating a single agent with basic tools to building complex, multi-agent systems. You'll learn how to equip your agents with a variety of tools, integrate with external services using the [**Model Context Protocol (MCP)**](https://modelcontextprotocol.io/overview), and orchestrate sophisticated workflows. We'll also explore the [**Agent-to-Agent (A2A) protocol**](https://a2a-protocol.org/latest/), a key feature for enabling seamless communication between different agents. Finally, you'll see how to deploy your agents to a scalable, fully managed environment with **Agent Engine**.

---

## Workshop Objectives
In this workshop, you will learn to:

* **Understand** the fundamental concepts of ADK.
* **Equip** agents with tools, including pre-built tools like Google Search and LangChain tools, and create custom tools from Python functions.
* **Integrate** with external services using the **Model Context Protocol (MCP)**, acting as both an MCP client and server.
* **Utilize** the **Agent-to-Agent (A2A) protocol** for complex communication between agents.
* **Build** multi-agent systems by defining relationships between agents and managing their interaction.
* **Orchestrate** complex agent workflows using dedicated workflow agents (Sequential, Parallel, and Loop).
* **Deploy** your agents to **Agent Engine** for a scalable, production-ready environment.

## Getting Started

To prepare your environment for this workshop, follow these steps:

1.  **Enable Vertex AI recommended APIs** see Step 3 from this [guide](https://cloud.google.com/vertex-ai/docs/start/cloud-environment#set_up_a_project)
2.  **Clone this repository** to get the workshop materials:
    ```
    git clone https://github.com/GCPartner/adk_workshop.git
    cd adk_workshop
    ```
3.  **Create a new Python virtual environment** and activate it:
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    ```
4.  **Install ADK and required dependencies**:
    ```
    python3 -m pip install -r requirements.txt
    ```
    If you are not using a virtual environment you can add the installation direction to your PATH
    ```
    echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
    source ~/.bashrc
    ```

5.  **Rename the `dotenv.example` file to `.env` file** and configure your global parameters, including your GCP Project, Location, and Default Model:
    ```
    GOOGLE_GENAI_USE_VERTEXAI=1
    GOOGLE_CLOUD_PROJECT=<YOUR_PROJECT_ID>
    GOOGLE_CLOUD_LOCATION=us-central1
    MODEL==gemini-2.0-flash-001
    ```

    
    ```
    mv dotenv.example .env
    ```

## Workshop Modules

1. [Introduction to ADK and its tools](adk_tools) with MCP and A2A
2. [Multi-Agent design](adk_multiagent_systems)
3. [Deploy to Agent Engine](adk_to_agent_engine)
-----
