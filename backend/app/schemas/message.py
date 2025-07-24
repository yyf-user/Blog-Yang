from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class MessageBase(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    is_read: bool


class MessageOut(MessageBase):
    id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True 