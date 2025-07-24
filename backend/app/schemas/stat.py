from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class StatBase(BaseModel):
    key: str
    value: int
    display_text: str


class StatCreate(StatBase):
    pass


class StatUpdate(StatBase):
    key: Optional[str] = None
    value: Optional[int] = None
    display_text: Optional[str] = None


class StatOut(StatBase):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True 