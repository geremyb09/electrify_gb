from typing import List, Optional, Tuple
import time
import pandas as pd
from anthropic import Anthropic
from langchain_core.messages import AIMessage

from config import (
    ANTHROPIC_API_KEY,
    ANTHROPIC_MODEL,
    ANTHROPIC_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY,
    DEFAULT_MAX_TOKENS
)
from src.state import AgentState


def get_anthropic_client(timeout: float = ANTHROPIC_TIMEOUT) -> Optional[Anthropic]:
    """
    Initialize and return Anthropic client with API key from environment.

    Args:
        timeout: Request timeout in seconds

    Returns:
        Anthropic client or None if API key not found
    """
    if not ANTHROPIC_API_KEY:
        return None
    return Anthropic(api_key=ANTHROPIC_API_KEY, timeout=timeout)


def call_claude_with_retry(
        client: Anthropic,
        prompt: str,
        max_retries: int = MAX_RETRIES,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = 0.7,
        operation_name: str = "API call"
) -> Tuple[str, bool]:
    """
    Call Claude API with exponential backoff retry logic.

    Args:
        client: Anthropic client instance
        prompt: The prompt to send to Claude
        max_retries: Maximum number of retry attempts
        max_tokens: Maximum tokens in response
        temperature: Sampling temperature
        operation_name: Name of operation for logging

    Returns:
        Tuple of (response_text, success_boolean)
    """
    retry_delay = RETRY_DELAY

    for attempt in range(max_retries):
        try:
            print(f"{operation_name} (attempt {attempt + 1}/{max_retries})...")

            message = client.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text
            print(f"{operation_name} complete!")
            return response_text, True

        except Exception as e:
            error_type = type(e).__name__

            if attempt < max_retries - 1:
                wait_time = retry_delay * (2 ** attempt)
                print(f"Attempt {attempt + 1} failed: {error_type}")
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                error_msg = (
                    f"Error after {max_retries} attempts: {error_type}\n\n"
                    f"Details: {str(e)}\n\n"
                )
                return error_msg, False

    return "Unexpected error in retry logic", False


def add_message_to_state(state: AgentState, content: str) -> AgentState:
    """
    Helper function to add a message to state and return updated state.

    Args:
        state: Current agent state
        content: Message content to add

    Returns:
        Updated AgentState with new message
    """
    return AgentState(
        messages=state.messages + [AIMessage(content=content)],
        raw_data=state.raw_data,
        top_performers=state.top_performers,
        filtered_data=state.filtered_data,
        title_patterns=state.title_patterns,
        generated_titles=state.generated_titles,
        channel_id=state.channel_id,
        top_n=state.top_n,
        new_video_summary=state.new_video_summary
    )


def format_titles_with_views(df: pd.DataFrame) -> List[dict]:
    """
    Format DataFrame titles with view counts for template rendering.

    Args:
        df: DataFrame with 'title' and 'views_in_period' columns

    Returns:
        List of dicts with title and view count
    """
    titles = []
    for idx, row in df.iterrows():
        titles.append({
            'title': row['title'],
            'views': row['views_in_period']
        })
    return titles


def get_example_titles(df: pd.DataFrame, n: int = 5) -> List[str]:
    """
    Extract top N titles from DataFrame for examples.

    Args:
        df: Pandas DataFrame with 'title' column
        n: Number of titles to extract

    Returns:
        List of title strings
    """
    return [row['title'] for _, row in df.head(n).iterrows()]
