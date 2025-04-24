import os
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv
from src.ai_agent.graph import AgentState
from src.ai_agent.tools import get_all_tools
from langchain_openai import ChatOpenAI


def get_llm():
    """Return configured LLM instance."""
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(model='gpt-4', api_key=openai_api_key)
    return llm.bind_tools(get_all_tools(), parallel_tool_calls=False)


def research_assistant(state: AgentState) -> AgentState:
    """Research assistant node implementation."""
    llm_with_tools = get_llm()
    sys_msg = SystemMessage(content="You are a helpful research assistant")
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

