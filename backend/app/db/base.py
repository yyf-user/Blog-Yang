"""
数据库基础模块

这个模块导入所有的数据库模型，以便Tortoise ORM可以发现它们。
当运行生成数据库架构或运行查询时，这些导入确保所有模型都被加载。
"""

# 用户相关
from app.models.user import User

# 内容相关
from app.models.article import Article, ArticleTag
from app.models.project import Project, ProjectTag
from app.models.tag import Tag
from app.models.skill import SkillCategory, Skill

# 通信相关
from app.models.message import Message
from app.models.subscriber import Subscriber

# 统计相关
from app.models.stat import Stat
from app.models.api_stat import ApiStat, ApiStatDaily

# 导出所有模型以便可以在其他地方使用
__all__ = [
    # 用户
    "User",
    
    # 内容
    "Article", "ArticleTag",
    "Project", "ProjectTag",
    "Tag",
    "SkillCategory", "Skill",
    
    # 通信
    "Message",
    "Subscriber",
    
    # 统计
    "Stat",
    "ApiStat", "ApiStatDaily",
] 