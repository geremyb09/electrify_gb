import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = "claude-sonnet-4-20250514"
ANTHROPIC_TIMEOUT = 120.0

# Data Configuration
DATA_PATH = "data/electrify__applied_ai_engineer__training_data.csv"
PROMPTS_DIR = "prompts"

# Agent Configuration
DEFAULT_TOP_N = 15
MAX_RETRIES = 3
RETRY_DELAY = 2

# Model Parameters
DEFAULT_MAX_TOKENS = 1500
PATTERN_ANALYSIS_TEMPERATURE = 0.7
TITLE_GENERATION_TEMPERATURE = 0.8
