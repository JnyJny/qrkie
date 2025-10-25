"""qrkie Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for qrkie."""

    model_config = SettingsConfigDict(
        env_prefix="QRKIE",
        env_file=".env-qrkie",
    )
    debug: bool = False
