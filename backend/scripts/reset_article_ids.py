#!/usr/bin/env python
"""
重置文章ID脚本

此脚本用于重置数据库中的文章ID，使其从1开始连续递增。
使用此脚本可以解决文章ID不连续或从较大数字开始的问题。
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径，确保可以导入app模块
root_dir = Path(__file__).parents[1]
sys.path.append(str(root_dir))

from app.utils import reset_table_ids
from app.db import init_db, close_db


async def reset_article_ids():
    """重置文章ID为连续的1,2,3..."""
    print("正在初始化数据库连接...")
    await init_db()
    
    try:
        # 定义文章表与其关联表
        related_tables = [
            {
                "table": "article_tags",
                "fk": "article_id",
                "pk": "tag_id"
            }
        ]
        
        # 重置文章表ID
        await reset_table_ids("articles", related_tables)
        
        print("文章ID重置完成！现在文章ID从1开始连续递增。")
    finally:
        # 关闭数据库连接
        await close_db()


if __name__ == "__main__":
    asyncio.run(reset_article_ids()) 