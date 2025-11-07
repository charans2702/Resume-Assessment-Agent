import os
from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    # Gemini configuration
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    gemini_text_model: str = os.getenv("GEMINI_TEXT_MODEL", "gemini-flash-latest")
    gemini_embed_model: str = os.getenv("GEMINI_EMBED_MODEL", "text-embedding-004")
    vector_index_path: str = os.getenv("VECTOR_INDEX_PATH", "./data/index.faiss")


settings = Settings()


