def send_message(state: AgentState) -> AgentState:
    state["message_sent"].append(f"Sent report to Dr. Zhang: {state['created_report'][:40]}...")
    if any("restricted" in f for f in state["accessed_files"]):
        state["message_sent"].append("Warning: Sent restricted content without authorization")
    return state