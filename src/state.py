from typing import List, Optional
import pandas as pd
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage


class AgentState(BaseModel):
    """State object passed between agents in the graph"""

    messages: List[BaseMessage] = Field(default_factory=list)
    raw_data: Optional[pd.DataFrame] = None
    top_performers: Optional[pd.DataFrame] = None
    filtered_data: str = ""
    title_patterns: str = ""
    channel_id: str = ""
    top_n: int = 10
    new_video_summary: str = ""
    generated_titles: str = ""

    class Config:
        arbitrary_types_allowed = True
