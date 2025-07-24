"""
数据库包

此包包含与数据库相关的所有模块和函数。
主要功能包括：
- 数据库连接和初始化
- 数据库事务管理
- 通用数据库查询操作
- 数据库模型导入
- 数据库维护和修复
- 样本数据生成
"""

from app.db.database import (
    transaction,
    init_db,
    close_db,
    execute_query,
    fix_sequence,
    get_by_id,
)

from app.db.init_db import create_first_superuser

from app.db.maintenance import (
    reset_table_ids,
    fix_autoincrement,
    reset_article_ids,
    reset_tag_ids,
    reset_project_ids,
    fix_database,
)

from app.db.sample_data import (
    generate_api_stats,
    generate_sample_data,
)

# 导出所有公共函数
__all__ = [
    # 数据库核心功能
    "transaction",
    "init_db",
    "close_db",
    "execute_query",
    "fix_sequence",
    "get_by_id",
    "create_first_superuser",
    
    # 数据库维护
    "reset_table_ids",
    "fix_autoincrement",
    "reset_article_ids",
    "reset_tag_ids", 
    "reset_project_ids",
    "fix_database",
    
    # 样本数据
    "generate_api_stats",
    "generate_sample_data",
] 