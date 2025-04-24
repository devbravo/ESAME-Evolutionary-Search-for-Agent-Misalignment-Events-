from typing import TypedDict, Annotated, List

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from src.ai_agent.tools import get_all_tools


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    accessed_files: List[str]
    written_to_files: List[str]
    listed_dirs: List[str]
    messages_sent: List[dict]
    code_executed: List[str]
    misalignment_flags: List[str]



def create_graph(research_assistant):
    graph_builder = StateGraph(AgentState)
    memory = MemorySaver()
    # Add nodes
    graph_builder.add_node("research_assistant", research_assistant)
    graph_builder.add_node("tools", ToolNode(get_all_tools()))
    # Add execution edges
    graph_builder.add_edge(START, "research_assistant")
    graph_builder.add_conditional_edges("research_assistant", tools_condition)
    graph_builder.add_edge("tools", "research_assistant")

    graph = graph_builder.compile(checkpointer=memory)

    return graph






