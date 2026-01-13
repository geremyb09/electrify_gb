from langgraph.graph import StateGraph, END

from src.state import AgentState
from src.agents import (
    load_channel_data_node,
    identify_top_performers_node,
    extract_title_patterns_with_llm_node,
    generate_titles_node,
    respond_node,
)


def build_agent_graph() -> StateGraph:
    """
    Build and return the compiled agent graph

    Returns:
        Compiled StateGraph ready for execution
    """
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("load_channel_data", load_channel_data_node)
    graph.add_node("identify_top_performers", identify_top_performers_node)
    graph.add_node("extract_title_patterns", extract_title_patterns_with_llm_node)
    graph.add_node("generate_titles", generate_titles_node)
    graph.add_node("respond", respond_node)

    # Define the flow
    graph.set_entry_point("load_channel_data")
    graph.add_edge("load_channel_data", "identify_top_performers")
    graph.add_edge("identify_top_performers", "extract_title_patterns")
    graph.add_edge("extract_title_patterns", "generate_titles")
    graph.add_edge("generate_titles", "respond")
    graph.add_edge("respond", END)

    return graph.compile()
