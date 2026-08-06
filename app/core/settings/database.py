from pydantic import BaseModel


class DatabaseSettings(BaseModel):
    host: str
    port: int = 3306
    username: str
    password: str
    name: str

    @property
    def url(self) -> str:
        return (
            f"mysql+pymysql://"
            f"{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )