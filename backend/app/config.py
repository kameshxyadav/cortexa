# backend/app/config.py
import os
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # Basic settings loaded from .env
    LLM_PROVIDER: str = Field(default="gemini")
    LLM_MODEL_FAST: str = Field(default="gemini-embedding-fast")
    LLM_MODEL_STRONG: str = Field(default="gemini-strong")
    LLM_MODEL_VERIFIER: str = Field(default="gemini-verifier")
    EMBED_MODEL: str = Field(default="gemini-embedding")
    GEMINI_API_KEY: str = Field(default="")
    LLM_MODE: str = Field(default="cache")
    WHISPER_MODEL: str = Field(default="small")
    DATABASE_URL: str = Field(default="sqlite:///./data/app.db")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
