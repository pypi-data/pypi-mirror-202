from typing import List, Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str

    QABOT_DATABASE_URI: Optional[str] = None
    QABOT_CACHE_DATABASE_URI = "duckdb:///:memory:"
    QABOT_MODEL_NAME = "gpt-3.5-turbo"
    QABOT_TABLES: Optional[List[str]]
