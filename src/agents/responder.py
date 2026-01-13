from src.state import AgentState
from src.utils import add_message_to_state


def respond_node(state: AgentState) -> AgentState:
    """
    Agent 5: Responder - Formats and presents the results

    Args:
        state: Current agent state

    Returns:
        Updated agent state with final response
    """
    response_parts = [f"\n{'=' * 80}\nSUMMARY\n{'=' * 80}\n"]

    if state.title_patterns:
        response_parts.append(f"Pattern analysis complete for top {state.top_n} performing videos.")

    if state.generated_titles:
        title_count = state.generated_titles.count("**") // 2
        response_parts.append(
            f"Generated {title_count} title options for your new video.\n"
            f"Use these optimized titles to maximize views and engagement!"
        )
    elif state.new_video_summary:
        response_parts.append("Title generation was requested but could not be completed.")
    else:
        response_parts.append(
            "No video summary provided - only pattern analysis performed.\n"
            "To generate titles, provide a new_video_summary parameter."
        )

    return add_message_to_state(state, "\n".join(response_parts))
