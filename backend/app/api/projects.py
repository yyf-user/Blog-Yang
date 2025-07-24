from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.deps import get_current_active_superuser, get_current_active_user
from app.models.project import Project
from app.models.tag import Tag
from app.models.user import User
from app.schemas.project import (
    ProjectCreate,
    ProjectOut,
    ProjectDetail,
    ProjectUpdate,
)
from app.utils.slug import generate_slug

router = APIRouter()


@router.get("", response_model=List[ProjectOut])
async def read_projects(
    skip: int = 0,
    limit: int = 20,
    tag: Optional[str] = None,
    featured: Optional[bool] = None,
) -> Any:
    """
    获取项目列表
    """
    query = Project.all().prefetch_related("tags")
    
    # 添加过滤条件
    if tag:
        query = query.filter(tags__slug=tag)
    
    if featured is not None:
        query = query.filter(featured=featured)
    
    # 排序：按ID升序
    query = query.order_by("id")
    
    # 分页
    projects = await query.offset(skip).limit(limit)
    
    return projects


@router.post("", response_model=ProjectOut)
async def create_project(
    project_in: ProjectCreate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    创建新项目
    """
    # 生成slug
    slug = project_in.slug or generate_slug(project_in.title)
    
    # 检查slug是否已存在
    existing_slug = await Project.filter(slug=slug).first()
    if existing_slug:
        slug = f"{slug}-{hash(project_in.title) % 1000}"
    
    # 创建项目
    project = Project(
        title=project_in.title,
        slug=slug,
        description=project_in.description,
        image_url=project_in.image_url,
        github_url=project_in.github_url,
        live_url=project_in.live_url,
        featured=project_in.featured,
        emoji=project_in.emoji,
    )
    
    await project.save()
    
    # 添加标签
    if project_in.tags:
        tags = await Tag.filter(id__in=project_in.tags)
        await project.tags.add(*tags)
    
    # 重新查询项目，以包含标签关系
    result = await Project.filter(id=project.id).prefetch_related("tags").first()
    
    return result


@router.get("/{project_id}", response_model=ProjectDetail)
async def read_project(
    project_id: int,
) -> Any:
    """
    通过ID获取项目
    """
    project = await Project.filter(id=project_id).prefetch_related("tags").first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在",
        )
    
    return project


@router.get("/by-slug/{slug}", response_model=ProjectDetail)
async def read_project_by_slug(
    slug: str,
) -> Any:
    """
    通过slug获取项目
    """
    project = await Project.filter(slug=slug).prefetch_related("tags").first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在",
        )
    
    return project


@router.put("/{project_id}", response_model=ProjectOut)
async def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    更新项目
    """
    project = await Project.filter(id=project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在",
        )
    
    # 更新字段
    if project_in.title is not None:
        project.title = project_in.title
        
        # 如果提供了新标题但没有提供slug，则重新生成slug
        if project_in.slug is None:
            new_slug = generate_slug(project_in.title)
            # 检查slug是否已存在
            existing_slug = await Project.filter(slug=new_slug).exclude(id=project_id).first()
            if existing_slug:
                new_slug = f"{new_slug}-{hash(project_in.title) % 1000}"
            project.slug = new_slug
    
    if project_in.slug is not None:
        # 检查slug是否已存在
        existing_slug = await Project.filter(slug=project_in.slug).exclude(id=project_id).first()
        if existing_slug:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该slug已存在",
            )
        project.slug = project_in.slug
    
    if project_in.description is not None:
        project.description = project_in.description
    
    if project_in.image_url is not None:
        project.image_url = project_in.image_url
    
    if project_in.github_url is not None:
        project.github_url = project_in.github_url
    
    if project_in.live_url is not None:
        project.live_url = project_in.live_url
    
    if project_in.featured is not None:
        project.featured = project_in.featured
    
    if project_in.emoji is not None:
        project.emoji = project_in.emoji
    
    await project.save()
    
    # 如果提供了标签，更新标签
    if project_in.tags is not None:
        # 先清除旧标签
        await project.tags.clear()
        if project_in.tags:
            # 添加新标签
            tags = await Tag.filter(id__in=project_in.tags)
            await project.tags.add(*tags)
    
    # 重新查询项目，以包含标签关系
    result = await Project.filter(id=project.id).prefetch_related("tags").first()
    
    return result


@router.put("/{project_id}/stats", response_model=ProjectOut)
async def update_project_stats(
    project_id: int,
    stars: Optional[int] = None,
    forks: Optional[int] = None,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    更新项目GitHub统计信息
    """
    project = await Project.filter(id=project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在",
        )
    
    # 更新统计信息
    if stars is not None:
        project.stars_count = stars
    
    if forks is not None:
        project.forks_count = forks
    
    await project.save()
    
    # 重新查询项目，以包含关系
    result = await Project.filter(id=project.id).prefetch_related("tags").first()
    
    return result


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    删除项目
    """
    project = await Project.filter(id=project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在",
        )
    
    # 删除项目
    await project.delete()
    
    return {"message": "项目已删除"} 