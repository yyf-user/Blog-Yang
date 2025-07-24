"""
自动更新统计数据的模块

此模块定义了更新各种统计数据的函数，包括文章数、项目数、用户数等。
这些函数会被定时任务或后台任务调用。
"""

import logging
from datetime import datetime

from app.models.stat import Stat
from app.models.article import Article
from app.models.project import Project
from app.models.user import User
from app.models.message import Message
from app.models.api_stat import ApiStat
from app.db import transaction

logger = logging.getLogger(__name__)


async def update_all_stats():
    """
    更新所有统计数据
    """
    try:
        # 使用事务确保一致性
        async with transaction():
            await update_article_count()
            await update_project_count()
            await update_user_count()
            await update_message_count()
            await update_visitor_count()
        
        logger.info("所有统计数据更新完成")
    except Exception as e:
        logger.error(f"更新统计数据失败: {e}")


async def update_article_count():
    """
    更新文章数量统计
    """
    try:
        # 获取文章总数
        article_count = await Article.all().count()
        
        # 更新或创建统计数据
        stat, created = await Stat.get_or_create(
            key="articles",
            defaults={"value": article_count, "display_text": "文章数量"}
        )
        
        if not created:
            stat.value = article_count
            await stat.save()
        
        logger.info(f"文章数量统计更新完成: {article_count}")
    except Exception as e:
        logger.error(f"更新文章数量统计失败: {e}")


async def update_project_count():
    """
    更新项目数量统计
    """
    try:
        # 获取项目总数
        project_count = await Project.all().count()
        
        # 更新或创建统计数据
        stat, created = await Stat.get_or_create(
            key="projects",
            defaults={"value": project_count, "display_text": "项目数量"}
        )
        
        if not created:
            stat.value = project_count
            await stat.save()
        
        logger.info(f"项目数量统计更新完成: {project_count}")
    except Exception as e:
        logger.error(f"更新项目数量统计失败: {e}")


async def update_user_count():
    """
    更新用户数量统计
    """
    try:
        # 获取用户总数
        user_count = await User.all().count()
        
        # 更新或创建统计数据
        stat, created = await Stat.get_or_create(
            key="users",
            defaults={"value": user_count, "display_text": "用户数量"}
        )
        
        if not created:
            stat.value = user_count
            await stat.save()
        
        logger.info(f"用户数量统计更新完成: {user_count}")
    except Exception as e:
        logger.error(f"更新用户数量统计失败: {e}")


async def update_message_count():
    """
    更新消息数量统计
    """
    try:
        # 获取消息总数
        message_count = await Message.all().count()
        
        # 更新或创建统计数据
        stat, created = await Stat.get_or_create(
            key="messages",
            defaults={"value": message_count, "display_text": "消息数量"}
        )
        
        if not created:
            stat.value = message_count
            await stat.save()
        
        logger.info(f"消息数量统计更新完成: {message_count}")
    except Exception as e:
        logger.error(f"更新消息数量统计失败: {e}")


async def update_visitor_count():
    """
    更新访问人数统计 (基于API调用的独立用户)
    """
    try:
        # 获取独立用户数 (非空的user_id)
        unique_users = len(set(
            stat.user_id for stat in await ApiStat.all() 
            if stat.user_id is not None
        ))
        
        # 考虑匿名用户 (估算为总请求的10%)
        total_calls = await ApiStat.all().count()
        estimated_anonymous = int(total_calls * 0.1)
        
        # 总访问人数 = 独立用户 + 估算的匿名用户
        visitor_count = unique_users + estimated_anonymous
        
        # 更新或创建统计数据
        stat, created = await Stat.get_or_create(
            key="visitors",
            defaults={"value": visitor_count, "display_text": "访问人数"}
        )
        
        if not created:
            stat.value = visitor_count
            await stat.save()
        
        logger.info(f"访问人数统计更新完成: {visitor_count} (独立用户: {unique_users}, 估算匿名: {estimated_anonymous})")
    except Exception as e:
        logger.error(f"更新访问人数统计失败: {e}") 