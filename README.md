## Architecture Design

```
┌───────────────────────────────────────────────────────────────────────┐
│                           YouTube Title Generator                     │
│                                                                       │
│  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐   │
│  │   CLI Client │◄───────►│  FastAPI     │◄───────►│  LangGraph   │   │
│  │   (Rich UI)  │   HTTP  │  Endpoint    │  State  │  Orchestrator│   │
│  └──────────────┘         └──────────────┘         └──────┬───────┘   │
│                           ┌───────────────────────────────┘           │
│                           ▼                                           │
│              ┌────────────────────────┐                               │
│              │   Multi-Agent System   │                               │
│              │  ┌──────────────────┐  │                               │
│              │  │ Data Retriever   │  │                               │
│              │  └────────┬─────────┘  │                               │
│              │           ▼            │                               │
│              │  ┌──────────────────┐  │                               │
│              │  │ Performance      │  │                               │
│              │  │ Analyzer         │  │                               │
│              │  └────────┬─────────┘  │                               │
│              │           ▼            │                               │
│              │  ┌──────────────────┐  │                               │
│              │  │ Pattern          │  │                               │
│              │  │ Extractor (AI)   │  │                               │
│              │  └────────┬─────────┘  │                               │
│              │           ▼            │                               │
│              │  ┌──────────────────┐  │                               │
│              │  │ Title            │  │                               │
│              │  │ Generator (AI)   │  │                               │
│              │  └────────┬─────────┘  │                               │
│              │           ▼            │                               │
│              │  ┌──────────────────┐  │                               │
│              │  │ Responder        │  │                               │
│              │  └──────────────────┘  │                               │
│              └────────────────────────┘                               │
│                           │                                           │
│                           ▼                                           │
│              ┌────────────────────────┐                               │
│              │   Data Layer           │                               │
│              │  • CSV Data Store      │                               │
│              │  • Pydantic Models     │                               │
│              │  • State Management    │                               │
│              └────────────────────────┘                               │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

### Environment Management with UV
To install and setup local environment run the following command:

```
chmod +x ./scripts/install_uv_and_sync.sh
./scripts/install_and_activate_uv.sh
```

### Environment Variables
Create .env file with this variable.
```
ANTHROPIC_API_KEY=your-api-key-here
```

### FastAPI Endpoint

To deploy the FastAPI endpoint run the following command:

```
chmod +x ./scripts/run_fastapi_endpoint.sh
./scripts//run_fastapi_endpoint.sh
```

The FastAPI endpoint uses a request API with the following inputs:
- channel_id (str): The unique identifier of the YouTube channel.
- summary (str): A single-sentence summary of the YouTube video to generate
titles for.

To use the endpoint run the following command:

```
python client.py <channel_id> <video summary>
e.g. python client.py UC510QYlOlKNyhy_zdQxnGYw "A tutorial on AI apps"
```

### Agent Orchestrator
We use LangGraph to manage agent workflows which contains the following agents:
- DataRetrieval
  - Retrieves channel specific data from CSV using Pandas.
- PerformanceAnalyser
  - Retrieves top performing videos based on views.
- PatternExtractor
  - Extracts patterns from titles using Anthropic Claude models.
  - Checks for patterns such as:
    - structural patterns,
    - keywords & phrases
    - psychological hooks
    - length analysis
  - Provides top 5 recommendations.
- TitleGenerator
  - Generates 3-5 titles based on patterns along with reasoning based on a video summary input.
- Responder
  - Outputs responses from each state.

### Data Validation with Pydantic
The system uses **Pydantic v2** for robust data validation and type safety:
### Prompt Rendering with Jinja
**Jinja2** templates separate prompt engineering from Python code, making prompts:
- Easy to modify without touching code
- Version-controllable
- Testable independently
- Reusable across agents
### Display outputs to client with rich
Provides cleaner outputs in terminal. Ideally we have an application where outputs will be displayed.
### Pre-commit Hooks
Runs linters, formatting, checks for private keys and large files. TODO: add unit tests.
