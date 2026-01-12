from langchain_core.messages import AIMessage

from config import TITLE_GENERATION_TEMPERATURE
from src.state import AgentState
from src.utils import (
    get_anthropic_client,
    call_claude_with_retry,
    add_message_to_state,
    get_example_titles
)
from src.prompt_manager import prompt_manager


def generate_titles_node(state: AgentState) -> AgentState:
    """
    Agent 4: Title Generator - Creates new titles based on patterns

    Args:
        state: Current agent state

    Returns:
        Updated agent state with generated titles
    """
    # Skip if no summary provided
    if not state.new_video_summary:
        return state

    # Get Anthropic client
    client = get_anthropic_client()
    if not client or not state.title_patterns:
        return add_message_to_state(
            state,
            "Skipping title generation (missing API key or patterns)"
        )

    # Prepare example titles
    example_titles = get_example_titles(state.top_performers)

    # Render prompt using Jinja2 template
    prompt = prompt_manager.render(
        "title_generation.jinja2",
        video_summary=state.new_video_summary,
        pattern_analysis=state.title_patterns,
        example_titles=example_titles
    )

    # Call Claude API with retry logic
    generated_titles, success = call_claude_with_retry(
        client=client,
        prompt=prompt,
        temperature=TITLE_GENERATION_TEMPERATURE,
        operation_name="Title generation"
    )

    if success:
        message = "Generated Title Options:\n\n" + generated_titles
    else:
        message = generated_titles  # Error message already formatted
        generated_titles = ""

    return AgentState(
        messages=state.messages + [AIMessage(content=message)],
        raw_data=state.raw_data,
        top_performers=state.top_performers,
        filtered_data=state.filtered_data,
        title_patterns=state.title_patterns,
        generated_titles=generated_titles,
        channel_id=state.channel_id,
        top_n=state.top_n,
        new_video_summary=state.new_video_summary
    )
