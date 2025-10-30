from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    database_url: str = Field(
        "sqlite+aiosqlite:///./agenda.db",
        description="Database connection string.",
    )
    semantic_index_path: str = Field(
        "./semantic_index.pkl", description="Path to the semantic search index file."
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
