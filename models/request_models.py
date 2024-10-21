from pydantic import BaseModel

class VideoURLs(BaseModel):
    urls: list[str]
