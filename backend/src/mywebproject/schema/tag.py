from pydantic import BaseModel


class TagRead(BaseModel):
    name: str
    count: int
