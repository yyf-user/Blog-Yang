#!/usr/bin/env python
"""
修复SQLite自动递增ID脚本

此脚本用于修复SQLite数据库中的自动递增ID序列，
确保下一个生成的ID是连续的，解决ID跳跃的问题。
"""

import asyncio
import sys
import logging
from pathlib import Path

# 添加项目根目录到Python路径，确保可以导入app模块
root_dir = Path(__file__).parents[1]
sys.path.append(str(root_dir))

from app.db import init_db, close_db, execute_query
from app.core.config import settings

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


async def fix_autoincrement():
    """修复SQLite自动递增ID"""
    print("正在初始化数据库连接...")
    await init_db()
    
    try:
        # 确认是SQLite数据库
        if not settings.DATABASE_URL.startswith('sqlite'):
            print("此脚本仅适用于SQLite数据库")
            return
            
        # 1. 检查sqlite_sequence表是否存在
        result = await execute_query("SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence'")
        if len(result["results"]) == 0:
            print("sqlite_sequence表不存在，创建该表...")
            await execute_query("CREATE TABLE sqlite_sequence (name TEXT, seq INTEGER)")
        
        # 2. 获取所有表名
        result = await execute_query("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [row["name"] for row in result["results"]]
        
        print(f"发现 {len(tables)} 个表:")
        for table in tables:
            print(f"- {table}")
        
        # 3. 对每个表修复自动递增ID
        for table in tables:
            try:
                # 检查表是否有id列
                result = await execute_query(f"PRAGMA table_info({table})")
                columns = result["results"]
                id_column = next((col for col in columns if col["name"].lower() == 'id'), None)
                
                if id_column:
                    # 获取当前最大ID
                    result = await execute_query(f"SELECT MAX(id) as max_id FROM {table}")
                    max_id = result["results"][0]["max_id"] or 0
                    
                    # 更新sqlite_sequence表
                    await execute_query(
                        f"INSERT OR REPLACE INTO sqlite_sequence (name, seq) VALUES (?, ?)", 
                        [table, max_id]
                    )
                    
                    print(f"表 {table} 的自动递增ID已设置为 {max_id}")
            except Exception as e:
                print(f"修复表 {table} 的自动递增ID时出错: {e}")
        
        # 4. 显示更新后的sqlite_sequence表
        result = await execute_query("SELECT * FROM sqlite_sequence")
        sequences = result["results"]
        
        print("\n当前sqlite_sequence表内容:")
        for seq in sequences:
            print(f"表: {seq['name']}, 下一个ID: {seq['seq'] + 1}")
        
        print("\n自动递增ID修复完成！")
        
    finally:
        # 关闭数据库连接
        await close_db()


if __name__ == "__main__":
    asyncio.run(fix_autoincrement()) 