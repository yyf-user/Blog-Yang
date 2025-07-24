from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.tag import TagOut


class ProjectBase(BaseModel):
    title: str
    description: str
    image_url: Optional[str] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    featured: Optional[bool] = False
    emoji: Optional[str] = "🚀"
    stars_count: Optional[int] = 0
    forks_count: Optional[int] = 0


class ProjectCreate(ProjectBase):
    slug: Optional[str] = None
    tags: List[int] = []


class ProjectUpdate(ProjectBase):
    title: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    tags: Optional[List[int]] = None


class ProjectOut(ProjectBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime
    tags: List[TagOut] = []

    class Config:
        from_attributes = True


class ProjectDetail(ProjectOut):
    pass 