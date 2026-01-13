from langchain_core.messages import AIMessage

from config import PATTERN_ANALYSIS_TEMPERATURE
from src.state import AgentState
from src.utils import (
    get_anthropic_client,
    call_claude_with_retry,
    add_message_to_state,
    format_titles_with_views,
)
from src.prompt_manager import prompt_manager


def extract_title_patterns_with_llm_node(state: AgentState) -> AgentState:
    """
    Agent 3: LLM Pattern Extractor - Uses Claude to analyze title patterns

    Args:
        state: Current agent state

    Returns:
        Updated agent state with extracted patterns
    """
    if state.top_performers is None or state.top_performers.empty:
        return add_message_to_state(state, "No top performers to analyze.")

    # Get Anthropic client
    client = get_anthropic_client()
    if not client:
        error_msg = (
            "ANTHROPIC_API_KEY not found!\n\n"
            "Please create a .env file in your project root with:\n"
            "ANTHROPIC_API_KEY=your-api-key-here"
        )
        return add_message_to_state(state, error_msg)

    # Prepare data for analysis
    titles_data = format_titles_with_views(state.top_performers)

    # Render prompt using Jinja2 template
    prompt = prompt_manager.render("pattern_analysis.jinja2", top_n=state.top_n, titles=titles_data)

    # Call Claude API with retry logic
    pattern_analysis, success = call_claude_with_retry(
        client=client,
        prompt=prompt,
        temperature=PATTERN_ANALYSIS_TEMPERATURE,
        operation_name="Pattern extraction",
    )

    if success:
        message = "AI-Powered Title Pattern Analysis:\n\n" + pattern_analysis
    else:
        message = pattern_analysis  # Error message already formatted
        pattern_analysis = ""

    return AgentState(
        messages=state.messages + [AIMessage(content=message)],
        raw_data=state.raw_data,
        top_performers=state.top_performers,
        filtered_data=state.filtered_data,
        title_patterns=pattern_analysis,
        channel_id=state.channel_id,
        top_n=state.top_n,
        new_video_summary=state.new_video_summary,
    )
