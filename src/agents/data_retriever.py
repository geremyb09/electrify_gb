"""Agent 1: Data Retriever"""
import pandas as pd
from langchain_core.messages import AIMessage

from config import DATA_PATH
from src.state import AgentState


def load_channel_data_node(state: AgentState) -> AgentState:
    """
    Agent 1: Data Retriever - Loads and filters data by channel_id

    Args:
        state: Current agent state

    Returns:
        Updated agent state with loaded data
    """
    df = pd.read_csv(DATA_PATH)

    # Filter by channel_id and select relevant columns
    df_filtered = df[df["channel_id"] == state.channel_id][
        ['channel_id', 'video_id', 'title', 'summary', 'views_in_period']
    ]

    message = f"Retrieved {len(df_filtered)} videos for channel {state.channel_id}"

    return AgentState(
        messages=state.messages + [AIMessage(content=message)],
        raw_data=df_filtered,
        channel_id=state.channel_id,
        top_n=state.top_n,
        new_video_summary=state.new_video_summary
    )
