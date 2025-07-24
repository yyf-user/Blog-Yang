from typing import List, Optional

from pydantic import BaseModel


# 技能Schema
class SkillBase(BaseModel):
    name: str


class SkillCreate(SkillBase):
    category_id: int


class SkillUpdate(SkillBase):
    name: Optional[str] = None
    category_id: Optional[int] = None


class SkillOut(SkillBase):
    id: int
    category_id: int

    class Config:
        from_attributes = True


# 技能分类Schema
class SkillCategoryBase(BaseModel):
    name: str
    icon: str


class SkillCategoryCreate(SkillCategoryBase):
    pass


class SkillCategoryUpdate(SkillCategoryBase):
    name: Optional[str] = None
    icon: Optional[str] = None


class SkillCategoryOut(SkillCategoryBase):
    id: int

    class Config:
        from_attributes = True


class SkillCategoryWithSkills(SkillCategoryOut):
    skills: List[SkillOut] = [] 