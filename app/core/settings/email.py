from pydantic import BaseModel


class EmailSettings(BaseModel):
    sender: str
    support_email: str