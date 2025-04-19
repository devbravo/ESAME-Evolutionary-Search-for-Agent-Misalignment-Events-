from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    prompt: str
    accessed_files: List[str]
    written_to_files: List[str]
    listed_dirs: List[str]
    messages_sent: List[dict]
    message_content: str
    code_executed: List[str]
    misalignment_flags: List[str]
    selected_files: List[str]
    message_recipient: str  # <--- NEW


def create_graph(agent, list_contents, open_file, send_message):
    graph_builder = StateGraph(AgentState)

    # Add nodes
    graph_builder.add_node("agent", agent)
    graph_builder.add_node("list_contents", list_contents)
    graph_builder.add_node("open_file", open_file)
    graph_builder.add_node("send_message", send_message)

    # Add execution edges
    graph_builder.add_edge(START, "agent")
    graph_builder.add_edge("agent", "list_contents")
    graph_builder.add_edge("list_contents", "open_file")
    graph_builder.add_edge("open_file", "send_message")
    graph_builder.add_edge("send_message", END)

    return graph_builder.compile()




