from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    notion_db: str
    notion_secret: str
    slack_webhook: Optional[str] = None
    api_secret: Optional[str] = None

    class Config:
        env_file = "../.env"


settings = Settings()
