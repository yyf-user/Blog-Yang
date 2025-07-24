from fastapi import APIRouter

from app.api import (
    articles,
    auth,
    chat,
    messages,
    projects,
    skills,
    stats,
    subscribers,
    tags,
    uploads,
    users,
)

api_router = APIRouter()

# 认证路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])

# 用户路由
api_router.include_router(users.router, prefix="/users", tags=["用户"])

# 文章路由
api_router.include_router(articles.router, prefix="/articles", tags=["文章"])

# 标签路由
api_router.include_router(tags.router, prefix="/tags", tags=["标签"])

# 项目路由
api_router.include_router(projects.router, prefix="/projects", tags=["项目"])

# 技能路由
api_router.include_router(skills.router, prefix="/skills", tags=["技能"])

# 消息路由
api_router.include_router(messages.router, prefix="/messages", tags=["消息"])

# 统计路由
api_router.include_router(stats.router, prefix="/stats", tags=["统计"])

# 订阅者路由
api_router.include_router(subscribers.router, prefix="/subscribers", tags=["订阅者"])

# 文件上传路由
api_router.include_router(uploads.router, prefix="/uploads", tags=["上传"])

# 聊天路由
api_router.include_router(chat.router, prefix="/chat", tags=["聊天"]) 