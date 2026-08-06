from pydantic import BaseModel


class AWSSettings(BaseModel):
    region: str
    s3_bucket: str