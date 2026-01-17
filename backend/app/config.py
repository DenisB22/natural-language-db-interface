import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "../data/ecommerce.db")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

LLM_DEBUG_DIR = os.getenv("LLM_DEBUG_DIR", "app/llm_debug")
LLM_DEBUG_ENABLED = os.getenv("LLM_DEBUG_ENABLED", "1") == "1"

