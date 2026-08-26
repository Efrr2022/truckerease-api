from pydantic import BaseModel


class AppSettings(BaseModel):
    name: str
    version: str
    environment: str
    debug: bool = False