from langchain_core.messages import AIMessage

from src.state import AgentState
from src.utils import add_message_to_state


def identify_top_performers_node(state: AgentState) -> AgentState:
    """
    Agent 2: Performance Analyzer - Identifies top performing videos

    Args:
        state: Current agent state

    Returns:
        Updated agent state with top performers identified
    """
    if state.raw_data is None or state.raw_data.empty:
        return add_message_to_state(state, "No data available to analyze.")

    # Get top N performers
    df_top = state.raw_data.nlargest(state.top_n, "views_in_period")

    # Calculate statistics
    total_views = df_top["views_in_period"].sum()
    avg_views = df_top["views_in_period"].mean()
    csv_text = df_top.to_string(index=False)

    message = (
        f"Identified top {len(df_top)} performing videos:\n"
        f"- Total views: {total_views:,}\n"
        f"- Average views: {avg_views:,.0f}\n"
    )

    return AgentState(
        messages=state.messages + [AIMessage(content=message)],
        raw_data=state.raw_data,
        top_performers=df_top,
        filtered_data=csv_text,
        channel_id=state.channel_id,
        top_n=state.top_n,
        new_video_summary=state.new_video_summary,
    )
