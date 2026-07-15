from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "DevOps RAG Assistant"
    knowledge_base_dir: Path = Path("../knowledge_base")
    storage_dir: Path = Path("./storage")
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    top_k: int = 4
    llm_provider: str = "none"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-1.5-flash"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def resolved_knowledge_base_dir(self) -> Path:
        return (Path(__file__).resolve().parents[2] / self.knowledge_base_dir).resolve()

    @property
    def resolved_storage_dir(self) -> Path:
        return (Path(__file__).resolve().parents[2] / self.storage_dir).resolve()


settings = Settings()
