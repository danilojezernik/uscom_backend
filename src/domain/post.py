import datetime
from typing import Optional

from pydantic import BaseModel, Field
from bson import ObjectId


class Post(BaseModel):
    id: Optional[str] = Field(alias='_id', default_factory=lambda: str(ObjectId()))
    post_title: str
    author: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at:  datetime.datetime = Field(default_factory=datetime.datetime.now)
