from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, \
                    StdioServerParameters, StdioConnectionParams

import sys
import os
sys.path.append("..")
from dotenv import load_dotenv
load_dotenv()

# IMPORTANT: Replace this with the ABSOLUTE path to your adk_server.py script
PATH_TO_YOUR_MCP_SERVER_SCRIPT = os.path.expandvars("$HOME/adk_workshop/adk_tools/adk_mcp_server/adk_server.py")
google_maps_api_key = os.environ.get("GOOGLE_MAPS_API_KEY")

if PATH_TO_YOUR_MCP_SERVER_SCRIPT == "None":
    print("WARNING: PATH_TO_YOUR_MCP_SERVER_SCRIPT is not set. Please update it in agent.py.")
    # Optionally, raise an error if the path is critical

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='web_reader_mcp_client_agent',
    instruction="Use the 'load_web_page' tool to fetch content from a URL provided by the user.",
    ## Add the MCPToolset below:

)