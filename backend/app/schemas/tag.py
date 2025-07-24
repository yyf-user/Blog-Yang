from pydantic import BaseModel
from typing import Optional


class TagBase(BaseModel):
    name: str
    slug: Optional[str] = None


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None


class TagOut(TagBase):
    id: int

    class Config:
        from_attributes = True 