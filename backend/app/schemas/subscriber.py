from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class SubscriberBase(BaseModel):
    email: EmailStr


class SubscriberCreate(SubscriberBase):
    pass


class SubscriberUpdate(BaseModel):
    status: str


class SubscriberOut(SubscriberBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True 