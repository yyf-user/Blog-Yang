"""
数据库核心模块

此模块是数据库功能的入口点，仅提供与app.db.database的兼容接口。
推荐直接使用app.db.database模块中的函数。
"""

# 从数据库模块导入所有功能
from app.db.database import (
    transaction as in_transaction,
    init_db,
    close_db,
    execute_query,
    fix_sequence,
    get_by_id,
)

# 为向后兼容性导出函数
__all__ = [
    "in_transaction",
    "init_db",
    "close_db",
    "execute_query", 
    "fix_sequence",
    "get_by_id",
    "get_database_url",
]


def get_database_url():
    """
    获取数据库URL
    """
    from app.core.config import settings
    return settings.DATABASE_URL 