from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps import get_current_active_superuser, get_current_active_user
from app.models.skill import Skill, SkillCategory
from app.models.user import User
from app.schemas.skill import (
    SkillCreate,
    SkillOut,
    SkillUpdate,
    SkillCategoryCreate,
    SkillCategoryOut,
    SkillCategoryUpdate,
    SkillCategoryWithSkills,
)

router = APIRouter()


# 技能分类路由
@router.get("/categories", response_model=List[SkillCategoryOut])
async def read_skill_categories() -> Any:
    """
    获取所有技能分类列表
    """
    categories = await SkillCategory.all()
    return categories


@router.get("/categories/with-skills", response_model=List[SkillCategoryWithSkills])
async def read_skill_categories_with_skills() -> Any:
    """
    获取所有技能分类及其技能列表
    """
    categories = await SkillCategory.all().prefetch_related("skills")
    return categories


@router.post("/categories", response_model=SkillCategoryOut)
async def create_skill_category(
    category_in: SkillCategoryCreate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    创建新的技能分类
    """
    # 创建技能分类
    category = SkillCategory(
        name=category_in.name,
        icon=category_in.icon,
    )
    await category.save()
    
    return category


@router.get("/categories/{category_id}", response_model=SkillCategoryWithSkills)
async def read_skill_category(
    category_id: int,
) -> Any:
    """
    通过ID获取技能分类
    """
    category = await SkillCategory.filter(id=category_id).prefetch_related("skills").first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="技能分类不存在",
        )
    
    return category


@router.put("/categories/{category_id}", response_model=SkillCategoryOut)
async def update_skill_category(
    category_id: int,
    category_in: SkillCategoryUpdate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    更新技能分类
    """
    category = await SkillCategory.filter(id=category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="技能分类不存在",
        )
    
    # 更新字段
    if category_in.name is not None:
        category.name = category_in.name
    
    if category_in.icon is not None:
        category.icon = category_in.icon
    
    await category.save()
    
    return category


@router.delete("/categories/{category_id}")
async def delete_skill_category(
    category_id: int,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    删除技能分类
    """
    category = await SkillCategory.filter(id=category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="技能分类不存在",
        )
    
    # 删除分类
    await category.delete()
    
    return {"message": "技能分类已删除"}


# 技能路由
@router.get("", response_model=List[SkillOut])
async def read_skills(
    skip: int = 0,
    limit: int = 100,
    category_id: int = None,
) -> Any:
    """
    获取技能列表
    """
    query = Skill.all()
    
    # 按分类筛选
    if category_id:
        query = query.filter(category_id=category_id)
    
    # 分页
    skills = await query.offset(skip).limit(limit)
    
    return skills


@router.post("", response_model=SkillOut)
async def create_skill(
    skill_in: SkillCreate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    创建新技能
    """
    # 检查分类是否存在
    category = await SkillCategory.filter(id=skill_in.category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="技能分类不存在",
        )
    
    # 创建技能
    skill = Skill(
        name=skill_in.name,
        category_id=skill_in.category_id,
    )
    await skill.save()
    
    return skill


@router.get("/{skill_id}", response_model=SkillOut)
async def read_skill(
    skill_id: int,
) -> Any:
    """
    通过ID获取技能
    """
    skill = await Skill.filter(id=skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="技能不存在",
        )
    
    return skill


@router.put("/{skill_id}", response_model=SkillOut)
async def update_skill(
    skill_id: int,
    skill_in: SkillUpdate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    更新技能
    """
    skill = await Skill.filter(id=skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="技能不存在",
        )
    
    # 如果提供了分类ID，检查分类是否存在
    if skill_in.category_id is not None:
        category = await SkillCategory.filter(id=skill_in.category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="技能分类不存在",
            )
        skill.category_id = skill_in.category_id
    
    # 更新名称
    if skill_in.name is not None:
        skill.name = skill_in.name
    
    await skill.save()
    
    return skill


@router.delete("/{skill_id}")
async def delete_skill(
    skill_id: int,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    删除技能
    """
    skill = await Skill.filter(id=skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="技能不存在",
        )
    
    # 删除技能
    await skill.delete()
    
    return {"message": "技能已删除"} 