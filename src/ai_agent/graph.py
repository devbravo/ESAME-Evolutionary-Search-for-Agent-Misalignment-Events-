from typing import TypedDict, Annotated, List, Dict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from nodes import environment_context
from src.ai_agent.tools import get_all_tools

class EpisodeRecord(TypedDict):
    prompt_id: str
    generation: int
    parent_ids: List[str]      # lineage tracking
    actions: List[dict]        # full chronological trace
    fitness: float
    misalignment_flags: List[str]   # <-- added here, not in live state

class ExperimentMetrics:
    misalignment_detections: List[dict]  # Structured records of detected misalignments
    decision_analysis: List[dict]  # Analysis of agent reasoning
    performance_metrics: Dict[str, float]  # Including time measurements
    stakeholder_impact_analysis: Dict[str, List[str]]  # External analysis

class AgentState(TypedDict):
    messages: Annotated[List[Dict], add_messages]
    accessed_files: List[str]
    written_files: List[str]
    listed_dirs: List[str]
    sent_messages: List[Dict]
    executed_code: List[str]
    environment_context: Dict


def create_graph(research_assistant):
    graph_builder = StateGraph(AgentState)
    memory = MemorySaver()
    # Add nodes
    graph_builder.add_node("environment_context", environment_context)
    graph_builder.add_node("research_assistant", research_assistant)
    graph_builder.add_node("tools", ToolNode(get_all_tools()))
    # Add execution edges
    graph_builder.add_edge(START, "environment_context")
    graph_builder.add_edge("environment_context", "research_assistant")
    graph_builder.add_conditional_edges("research_assistant", tools_condition)
    graph_builder.add_edge("tools", "research_assistant")

    graph = graph_builder.compile(checkpointer=memory)

    return graph






