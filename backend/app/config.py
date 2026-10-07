"""
GraphOps Configuration Module.

Loads environment variables and provides application-wide settings.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load .env file from backend directory
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)


class Neo4jSettings(BaseModel):
    """Neo4j connection settings loaded from environment variables."""

    uri: str = Field(default_factory=lambda: os.getenv("NEO4J_URI", ""))
    username: str = Field(default_factory=lambda: os.getenv("NEO4J_USERNAME", ""))
    password: str = Field(default_factory=lambda: os.getenv("NEO4J_PASSWORD", ""))
    database: str = Field(default_factory=lambda: os.getenv("NEO4J_DATABASE", "neo4j"))

    def validate_credentials(self) -> bool:
        """Return True if all required Neo4j credentials are provided."""
        return bool(self.uri and self.username and self.password)


class AppSettings(BaseModel):
    """Application-level settings."""

    app_name: str = "GraphOps"
    app_version: str = "0.1.0"
    debug: bool = Field(
        default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true"
    )
    cors_origins: list[str] = Field(
        default_factory=lambda: os.getenv(
            "CORS_ORIGINS", "http://localhost:5173"
        ).split(",")
    )


# Singleton instances
neo4j_settings = Neo4jSettings()
app_settings = AppSettings()
