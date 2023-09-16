import datetime
from typing import Optional

from pydantic import BaseModel, Field
from bson import ObjectId


class Comment(BaseModel):
    id: Optional[str] = Field(alias='_id', default_factory=lambda: str(ObjectId()))
    post_id: str
    content: str
    author: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
