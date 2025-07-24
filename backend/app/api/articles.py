import datetime
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.deps import get_current_active_superuser, get_current_active_user
from app.models.article import Article
from app.models.tag import Tag
from app.models.user import User
from app.schemas.article import (
    ArticleCreate,
    ArticleOut,
    ArticleDetail,
    ArticlePublish,
    ArticleUpdate,
)
from app.utils.slug import generate_slug

router = APIRouter()


@router.get("", response_model=List[ArticleOut])
async def read_articles(
    skip: int = 0,
    limit: int = 20,
    tag: Optional[str] = None,
    featured: Optional[bool] = None,
    status: Optional[str] = "published",
) -> Any:
    """
    获取文章列表
    """
    query = Article.all().prefetch_related("author", "tags")
    
    # 添加过滤条件
    if tag:
        query = query.filter(tags__slug=tag)
    
    if featured is not None:
        query = query.filter(featured=featured)
    
    if status:
        query = query.filter(status=status)
    
    # 排序：按ID升序
    query = query.order_by("id")
    
    # 分页
    articles = await query.offset(skip).limit(limit)
    
    return articles


@router.post("", response_model=ArticleOut)
async def create_article(
    article_in: ArticleCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    创建新文章
    """
    # 生成slug
    slug = article_in.slug or generate_slug(article_in.title)
    
    # 检查slug是否已存在
    existing_slug = await Article.filter(slug=slug).first()
    if existing_slug:
        slug = f"{slug}-{hash(article_in.title) % 1000}"
    
    # 计算阅读时间（大约每分钟200字）
    text_length = len(article_in.content)
    read_time = max(1, text_length // 200)
    
    # 创建文章
    article = Article(
        title=article_in.title,
        slug=slug,
        excerpt=article_in.excerpt,
        content=article_in.content,
        cover_image=article_in.cover_image,
        featured=article_in.featured,
        status=article_in.status,
        read_time=read_time,
        author_id=current_user.id,
    )
    
    # 如果是已发布状态，设置发布时间
    if article.status == "published":
        article.published_at = datetime.datetime.now()
    
    await article.save()
    
    # 添加标签
    if article_in.tags:
        tags = await Tag.filter(id__in=article_in.tags)
        await article.tags.add(*tags)
    
    # 重新查询文章，以包含标签关系
    result = await Article.filter(id=article.id).prefetch_related("author", "tags").first()
    
    return result


@router.get("/{article_id}", response_model=ArticleDetail)
async def read_article(
    article_id: int,
) -> Any:
    """
    通过ID获取文章
    """
    article = await Article.filter(id=article_id).prefetch_related("author", "tags").first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在",
        )
    
    # 增加阅读量
    article.view_count += 1
    await article.save()
    
    return article


@router.get("/by-slug/{slug}", response_model=ArticleDetail)
async def read_article_by_slug(
    slug: str,
) -> Any:
    """
    通过slug获取文章
    """
    article = await Article.filter(slug=slug).prefetch_related("author", "tags").first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在",
        )
    
    # 增加阅读量
    article.view_count += 1
    await article.save()
    
    return article


@router.put("/{article_id}", response_model=ArticleOut)
async def update_article(
    article_id: int,
    article_in: ArticleUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    更新文章
    """
    article = await Article.filter(id=article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在",
        )
    
    # 检查权限：只有作者或管理员可以更新
    if article.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足",
        )
    
    # 更新字段
    if article_in.title is not None:
        article.title = article_in.title
        
        # 如果提供了新标题但没有提供slug，则重新生成slug
        if article_in.slug is None:
            new_slug = generate_slug(article_in.title)
            # 检查slug是否已存在
            existing_slug = await Article.filter(slug=new_slug).exclude(id=article_id).first()
            if existing_slug:
                new_slug = f"{new_slug}-{hash(article_in.title) % 1000}"
            article.slug = new_slug
    
    if article_in.slug is not None:
        # 检查slug是否已存在
        existing_slug = await Article.filter(slug=article_in.slug).exclude(id=article_id).first()
        if existing_slug:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该slug已存在",
            )
        article.slug = article_in.slug
    
    if article_in.excerpt is not None:
        article.excerpt = article_in.excerpt
    
    if article_in.content is not None:
        article.content = article_in.content
        # 重新计算阅读时间
        text_length = len(article_in.content)
        article.read_time = max(1, text_length // 200)
    
    if article_in.cover_image is not None:
        article.cover_image = article_in.cover_image
    
    if article_in.featured is not None:
        article.featured = article_in.featured
    
    if article_in.status is not None:
        article.status = article_in.status
        # 如果从草稿变为已发布状态，设置发布时间
        if article.status == "published" and article.published_at is None:
            article.published_at = datetime.datetime.now()
    
    await article.save()
    
    # 如果提供了标签，更新标签
    if article_in.tags is not None:
        # 先清除旧标签
        await article.tags.clear()
        if article_in.tags:
            # 添加新标签
            tags = await Tag.filter(id__in=article_in.tags)
            await article.tags.add(*tags)
    
    # 重新查询文章，以包含标签关系
    result = await Article.filter(id=article.id).prefetch_related("author", "tags").first()
    
    return result


@router.put("/{article_id}/publish", response_model=ArticleOut)
async def publish_article(
    article_id: int,
    publish_in: ArticlePublish,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    发布文章
    """
    article = await Article.filter(id=article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在",
        )
    
    # 检查权限：只有作者或管理员可以发布
    if article.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足",
        )
    
    # 更新状态
    article.status = publish_in.status
    
    # 设置发布时间
    if publish_in.status == "published" and article.published_at is None:
        article.published_at = datetime.datetime.now()
    
    await article.save()
    
    # 重新查询文章，以包含关系
    result = await Article.filter(id=article.id).prefetch_related("author", "tags").first()
    
    return result


@router.delete("/{article_id}")
async def delete_article(
    article_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    删除文章
    """
    article = await Article.filter(id=article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在",
        )
    
    # 检查权限：只有作者或管理员可以删除
    if article.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足",
        )
    
    # 删除文章
    await article.delete()
    
    return {"message": "文章已删除"} 