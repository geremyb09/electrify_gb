from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from langchain_core.messages import HumanMessage
from contextlib import asynccontextmanager
import logging

from config import DEFAULT_TOP_N
from src.state import AgentState
from src.graph import build_agent_graph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
agent_graph = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler"""
    # Startup
    global agent_graph
    logger.info("Building agent graph...")
    agent_graph = build_agent_graph()
    logger.info("Agent graph ready!")

    yield

    # Shutdown (cleanup if needed)
    logger.info("Shutting down...")

app = FastAPI(
    title="YouTube Title Optimizer API",
    description="Generate optimized YouTube video titles",
    version="1.0.0",
    lifespan=lifespan
)


# Request/Response Models
class TitleRequest(BaseModel):
    channel_id: str = Field(..., description="YouTube channel ID")
    summary: str = Field(..., description="Video summary")
    top_n: Optional[int] = Field(DEFAULT_TOP_N, ge=5, le=50)


class TitleResponse(BaseModel):
    channel_id: str
    summary: str
    pattern_analysis: str
    generated_titles: str
    metadata: dict

@app.get("/")
async def root():
    return {"message": "YouTube Title Optimizer API", "status": "healthy"}

@app.get("/health")
async def health():
    return {"status": "healthy", "graph_ready": agent_graph is not None}


@app.post("/generate-titles", response_model=TitleResponse)
async def generate_titles(request: TitleRequest):
    """Generate optimized YouTube titles"""
    try:
        # Run agent graph
        result = agent_graph.invoke(
            AgentState(
                messages=[HumanMessage(content="Generate titles")],
                channel_id=request.channel_id,
                top_n=request.top_n,
                new_video_summary=request.summary
            )
        )

        # Extract text from messages
        pattern_analysis = ""
        generated_titles = ""

        for msg in result["messages"]:
            content = msg.content
            if "Pattern Analysis:" in content:
                pattern_analysis = content.split("Pattern Analysis:")[1].strip()
            elif "Generated Title Options:" in content:
                generated_titles = content.split("Generated Title Options:")[1].strip()

        return TitleResponse(
            channel_id=request.channel_id,
            summary=request.summary,
            pattern_analysis=pattern_analysis,
            generated_titles=generated_titles,
            metadata={
                "top_n": request.top_n,
                "total_videos": len(result["raw_data"]) if result["raw_data"] is not None else 0,
                "avg_views": int(result["top_performers"]['views_in_period'].mean())
            }
        )

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)