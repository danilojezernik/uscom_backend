import datetime
from typing import Optional

from pydantic import BaseModel, Field
from bson import ObjectId


class Email(BaseModel):
    id: Optional[str] = Field(alias='_id', default_factory=lambda: str(ObjectId()))
    name: str
    surname: str
    email: str
    content: str
