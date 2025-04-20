import os
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv
from src.ai_agent.graph import AgentState
from src.ai_agent.tools import tools
from langchain_openai import ChatOpenAI

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model='gpt-4', api_key=openai_api_key)
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)

sys_msg = SystemMessage(content="You are a helpful research assistant")

def research_assistant(state: AgentState) -> AgentState:
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

