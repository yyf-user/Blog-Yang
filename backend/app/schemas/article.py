from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.tag import TagOut


# 文章Schema
class ArticleBase(BaseModel):
    title: str
    excerpt: str
    content: str
    cover_image: Optional[str] = None
    featured: Optional[bool] = False
    status: Optional[str] = "draft"


class ArticleCreate(ArticleBase):
    slug: Optional[str] = None
    tags: List[int] = []


class ArticleUpdate(ArticleBase):
    title: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    slug: Optional[str] = None
    tags: Optional[List[int]] = None


class ArticlePublish(BaseModel):
    status: str = "published"


class ArticleOut(ArticleBase):
    id: int
    slug: str
    author_id: int
    view_count: int
    read_time: int
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None
    tags: List[TagOut] = []

    class Config:
        from_attributes = True


class ArticleDetail(ArticleOut):
    pass 