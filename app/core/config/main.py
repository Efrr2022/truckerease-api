from pydantic_settings import BaseSettings, SettingsConfigDict

from .app import AppSettings
from .database import DatabaseSettings
from .security import SecuritySettings
from .aws import AWSSettings
from .email import EmailSettings
from .logging import LoggingSettings


class Settings(BaseSettings):

    app: AppSettings
    database: DatabaseSettings
    security: SecuritySettings
    aws: AWSSettings
    email: EmailSettings
    logging: LoggingSettings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore",
    )