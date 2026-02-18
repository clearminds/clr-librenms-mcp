"""Configuration for LibreNMS MCP Server."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings loaded from environment variables."""

    librenms_url: str = ""
    librenms_token: str = ""
    librenms_transport: str = "stdio"
    librenms_log_level: str = "INFO"

    model_config = {"env_prefix": ""}

    # Map to env vars: LIBRENMS_URL, LIBRENMS_TOKEN
