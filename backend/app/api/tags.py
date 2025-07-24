from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from tortoise.exceptions import DoesNotExist

from app.models.tag import Tag
from app.core.deps import get_current_active_user, get_current_active_superuser
from app.schemas.tag import TagCreate, TagOut, TagUpdate
from app.utils.slug import generate_slug
from app.db import transaction

router = APIRouter()

@router.get("", response_model=List[TagOut])
async def read_tags() -> Any:
    """
    获取所有标签
    """
    tags = await Tag.all().order_by("id")
    return tags


@router.post("", response_model=TagOut)
async def create_tag(
    tag_in: TagCreate,
    current_user: Any = Depends(get_current_active_superuser),
) -> Any:
    """
    创建新标签
    """
    # 检查标签名是否已存在
    existing_tag = await Tag.filter(name=tag_in.name).first()
    if existing_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该标签已存在",
        )
    
    # 生成slug
    slug = tag_in.slug or generate_slug(tag_in.name)
    
    # 检查slug是否已存在
    existing_slug = await Tag.filter(slug=slug).first()
    if existing_slug:
        slug = f"{slug}-{hash(tag_in.name) % 1000}"
    
    try:
        # 查找当前最大ID
        max_id_tag = await Tag.all().order_by("-id").first()
        next_id = 1  # 默认从1开始
        
        if max_id_tag:
            next_id = max_id_tag.id + 1
            
        # 创建标签
        tag = Tag(name=tag_in.name, slug=slug)
        await tag.save()
        
        # 记录日志
        print(f"创建标签成功: ID={tag.id}, 名称={tag.name}, slug={tag.slug}")
        
        return tag
    except Exception as e:
        print(f"创建标签失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建标签失败: {str(e)}",
        )


@router.get("/{tag_id}", response_model=TagOut)
async def read_tag(tag_id: int) -> Any:
    """
    获取指定标签
    """
    tag = await Tag.filter(id=tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="标签不存在",
        )
    return tag


@router.put("/{tag_id}", response_model=TagOut)
async def update_tag(
    tag_id: int,
    tag_in: TagUpdate,
    current_user: Any = Depends(get_current_active_superuser),
) -> Any:
    """
    更新标签
    """
    tag = await Tag.filter(id=tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="标签不存在",
        )
    
    # 如果更新了名称，检查名称是否已存在
    if tag_in.name and tag_in.name != tag.name:
        existing_tag = await Tag.filter(name=tag_in.name).first()
        if existing_tag:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该标签名已存在",
            )
    
    # 如果更新了slug，检查slug是否已存在
    if tag_in.slug and tag_in.slug != tag.slug:
        existing_slug = await Tag.filter(slug=tag_in.slug).first()
        if existing_slug:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该slug已存在",
            )
    
    # 更新标签
    if tag_in.name:
        tag.name = tag_in.name
    if tag_in.slug:
        tag.slug = tag_in.slug
    await tag.save()
    
    return tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: int, current_user: Any = Depends(get_current_active_superuser)
):
    """
    删除标签
    """
    # 查找要删除的标签
    tag = await Tag.filter(id=tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="标签不存在",
        )
    
    # 获取删除前的最大ID，用于后续重排
    max_id = await Tag.all().count()
    
    # 删除标签
    await tag.delete()
    
    # 使用数据库事务自动重排ID
    async with transaction() as conn:
        try:
            # 1. 获取所有标签并按ID排序
            tags = await Tag.all().order_by('id')
            
            # 2. 更新每个标签的ID，使其连续
            for new_id, tag in enumerate(tags, 1):
                # 只有当ID不等于新ID时才更新
                if tag.id != new_id:
                    await Tag.filter(id=tag.id).update(id=new_id)
            
            # 3. 修复SQLite序列生成器
            # 获取当前最大ID
            count = await Tag.all().count()
            
            # 更新sqlite_sequence表
            await conn.execute_query(
                "UPDATE sqlite_sequence SET seq = ? WHERE name = 'tags'",
                [count]
            )
            
            # 4. 更新关联表中的外键引用
            # 修复文章与标签的关联
            article_tags = await conn.execute_query(
                "SELECT article_id, tag_id FROM article_tags ORDER BY tag_id"
            )
            
            # 删除现有关联
            await conn.execute_query("DELETE FROM article_tags")
            
            # 重新插入关联记录
            for article_id, old_tag_id in article_tags[1]:
                # 找到对应的新tag_id
                tag = await Tag.filter(id=old_tag_id).first()
                if tag:
                    await conn.execute_query(
                        "INSERT INTO article_tags (article_id, tag_id) VALUES (?, ?)",
                        [article_id, tag.id]
                    )
            
            # 修复项目与标签的关联
            project_tags = await conn.execute_query(
                "SELECT project_id, tag_id FROM project_tags ORDER BY tag_id"
            )
            
            # 删除现有关联
            await conn.execute_query("DELETE FROM project_tags")
            
            # 重新插入关联记录
            for project_id, old_tag_id in project_tags[1]:
                # 找到对应的新tag_id
                tag = await Tag.filter(id=old_tag_id).first()
                if tag:
                    await conn.execute_query(
                        "INSERT INTO project_tags (project_id, tag_id) VALUES (?, ?)",
                        [project_id, tag.id]
                    )
            
            print(f"标签ID已自动重排，当前共有 {count} 个标签")
            
        except Exception as e:
            print(f"重排标签ID时出错: {e}")
            # 事务会自动回滚 