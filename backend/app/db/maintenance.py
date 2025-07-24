"""
数据库维护模块

提供数据库维护、修复和数据重置功能。
这些功能主要用于开发和管理目的，不应在正常应用操作中使用。
"""

import logging
import asyncio
import sys
import sqlite3
from pathlib import Path
from typing import List, Dict, Optional, Any, Union

from app.db import transaction, execute_query, init_db, close_db
from app.core.config import settings
from app.models.api_stat import ApiStat, ApiStatDaily

logger = logging.getLogger(__name__)


async def reset_table_ids(
    table_name: str, 
    related_tables: Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    """
    重置表的ID，使其从1开始连续递增
    
    Args:
        table_name: 要重置ID的表名
        related_tables: 包含与此表有关联的表信息的列表，格式为：
                        [
                            {
                                "table": "关联表名",
                                "fk": "外键列名",
                                "pk": "主表主键列名（通常为'id'）"
                            }
                        ]
    
    Returns:
        结果信息字典
    """
    if not settings.DATABASE_URL.startswith('sqlite'):
        logger.warning("重置ID序列仅支持SQLite数据库")
        return {
            "success": False,
            "message": "重置ID序列仅支持SQLite数据库"
        }
    
    db_path = Path(settings.DATABASE_URL.replace("sqlite://", ""))
    
    if not db_path.exists():
        logger.error(f"数据库文件不存在: {db_path}")
        return {
            "success": False,
            "message": f"数据库文件不存在: {db_path}"
        }
    
    logger.info(f"开始重置表 {table_name} 的ID序列...")
    
    # 使用sqlite3直接操作数据库
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # 1. 创建临时表
        logger.info(f"创建临时表 {table_name}_temp...")
        cursor.execute(f"CREATE TABLE {table_name}_temp AS SELECT * FROM {table_name}")
        
        # 2. 删除原表
        logger.info(f"删除原表 {table_name}...")
        cursor.execute(f"DROP TABLE {table_name}")
        
        # 3. 获取表结构
        logger.info("获取表结构...")
        cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}_temp'")
        create_table_sql = cursor.fetchone()[0]
        create_table_sql = create_table_sql.replace(f'CREATE TABLE {table_name}_temp', f'CREATE TABLE {table_name}')
        
        # 4. 使用新的表结构重建表
        logger.info(f"重建表 {table_name}...")
        cursor.execute(create_table_sql)
        
        # 5. 获取所有数据，按ID排序
        logger.info(f"获取表 {table_name} 的数据...")
        cursor.execute(f"SELECT * FROM {table_name}_temp ORDER BY id")
        rows = cursor.fetchall()
        
        # 获取列名
        cursor.execute(f"PRAGMA table_info({table_name}_temp)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # 6. 插入数据，自动生成新的ID (从1开始)
        logger.info(f"插入数据，使用新的连续ID...")
        if rows:
            # 构建不包含id列的插入语句
            cols_without_id = [col for col in columns if col.lower() != 'id']
            placeholders = ', '.join(['?' for _ in cols_without_id])
            cols_str = ', '.join(cols_without_id)
            
            for row in rows:
                # 提取除了ID以外的所有列值
                values = [row[columns.index(col)] for col in cols_without_id]
                cursor.execute(f"INSERT INTO {table_name} ({cols_str}) VALUES ({placeholders})", values)
        
        # 7. 删除临时表
        logger.info(f"删除临时表 {table_name}_temp...")
        cursor.execute(f"DROP TABLE {table_name}_temp")
        
        # 8. 修复相关表的外键引用
        if related_tables:
            for related in related_tables:
                related_table = related["table"]
                fk_column = related["fk"]
                pk_column = related.get("pk", "id")
                
                logger.info(f"修复关联表 {related_table} 的外键引用...")
                
                # 获取关联表数据
                cursor.execute(f"SELECT * FROM {related_table}")
                related_rows = cursor.fetchall()
                
                # 获取关联表列名
                cursor.execute(f"PRAGMA table_info({related_table})")
                related_columns = [col[1] for col in cursor.fetchall()]
                
                # 获取主键和外键列的索引
                pk_idx = related_columns.index(pk_column) if pk_column in related_columns else None
                fk_idx = related_columns.index(fk_column) if fk_column in related_columns else None
                
                if pk_idx is not None and fk_idx is not None:
                    # 获取新旧ID的映射
                    cursor.execute(f"SELECT rowid, id FROM {table_name}")
                    id_mapping = {i: row_id for row_id, i in enumerate(range(1, len(cursor.fetchall()) + 1), 1)}
                    
                    # 删除关联表数据
                    cursor.execute(f"DELETE FROM {related_table}")
                    
                    # 重新插入关联表数据，使用新的ID
                    for row in related_rows:
                        old_fk = row[fk_idx]
                        if old_fk in id_mapping:
                            new_fk = id_mapping[old_fk]
                            
                            # 构建INSERT语句
                            cols = []
                            vals = []
                            for i, col in enumerate(related_columns):
                                if i == fk_idx:
                                    cols.append(col)
                                    vals.append(new_fk)
                                else:
                                    cols.append(col)
                                    vals.append(row[i])
                            
                            cols_str = ', '.join(cols)
                            placeholders = ', '.join(['?' for _ in cols])
                            cursor.execute(f"INSERT INTO {related_table} ({cols_str}) VALUES ({placeholders})", vals)
                else:
                    logger.warning(f"无法在关联表 {related_table} 中找到主键列 {pk_column} 或外键列 {fk_column}")
        
        # 9. 修复SQLite序列生成器
        logger.info("修复SQLite序列生成器...")
        cursor.execute(f"SELECT MAX(id) FROM {table_name}")
        max_id = cursor.fetchone()[0] or 0
        cursor.execute(f"UPDATE sqlite_sequence SET seq = {max_id} WHERE name = '{table_name}'")
        
        # 提交更改
        conn.commit()
        logger.info(f"表 {table_name} 的ID已重置为从1开始连续递增，当前最大ID: {max_id}")
        
        return {
            "success": True,
            "message": f"表 {table_name} 的ID已重置为从1开始连续递增",
            "max_id": max_id
        }
    except Exception as e:
        conn.rollback()
        logger.error(f"重置表 {table_name} 的ID时出错: {e}")
        return {
            "success": False,
            "message": f"重置表 {table_name} 的ID时出错: {e}"
        }
    finally:
        conn.close()


async def fix_autoincrement():
    """
    修复SQLite自动递增ID序列
    
    此函数检查所有表的自动递增ID序列，并确保它们设置为当前最大ID值，
    防止新建记录时ID出现跳跃。
    """
    try:
        # 确认是SQLite数据库
        if not settings.DATABASE_URL.startswith('sqlite'):
            logger.warning("此函数仅适用于SQLite数据库")
            return {
                "success": False,
                "message": "此函数仅适用于SQLite数据库"
            }
            
        # 1. 检查sqlite_sequence表是否存在
        result = await execute_query("SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence'")
        if len(result["results"]) == 0:
            logger.info("sqlite_sequence表不存在，创建该表...")
            await execute_query("CREATE TABLE sqlite_sequence (name TEXT, seq INTEGER)")
        
        # 2. 获取所有表名
        result = await execute_query("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [row["name"] for row in result["results"]]
        
        logger.info(f"发现 {len(tables)} 个表")
        
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
                    
                    logger.info(f"表 {table} 的自动递增ID已设置为 {max_id}")
            except Exception as e:
                logger.error(f"修复表 {table} 的自动递增ID时出错: {e}")
        
        # 4. 显示更新后的sqlite_sequence表
        result = await execute_query("SELECT * FROM sqlite_sequence")
        sequences = result["results"]
        
        logger.info("自动递增ID修复完成")
        return {
            "success": True,
            "message": "自动递增ID修复完成",
            "tables_fixed": len(tables),
            "sequences": sequences
        }
    except Exception as e:
        logger.error(f"修复自动递增ID时出错: {e}")
        return {
            "success": False,
            "message": f"修复自动递增ID时出错: {e}"
        }


async def reset_article_ids():
    """
    重置文章ID
    
    将文章表的ID重置为从1开始连续的序列，并修复关联关系。
    """
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
        result = await reset_table_ids("articles", related_tables)
        
        logger.info("文章ID重置完成")
        return result
    except Exception as e:
        logger.error(f"重置文章ID时出错: {e}")
        return {
            "success": False,
            "message": f"重置文章ID时出错: {e}"
        }


async def reset_tag_ids():
    """
    重置标签ID
    
    将标签表的ID重置为从1开始连续的序列，并修复关联关系。
    """
    try:
        # 定义标签表与其关联表
        related_tables = [
            {
                "table": "article_tags",
                "fk": "tag_id",
                "pk": "article_id"
            },
            {
                "table": "project_tags",
                "fk": "tag_id",
                "pk": "project_id"
            }
        ]
        
        # 重置标签表ID
        result = await reset_table_ids("tags", related_tables)
        
        logger.info("标签ID重置完成")
        return result
    except Exception as e:
        logger.error(f"重置标签ID时出错: {e}")
        return {
            "success": False,
            "message": f"重置标签ID时出错: {e}"
        }


async def reset_project_ids():
    """
    重置项目ID
    
    将项目表的ID重置为从1开始连续的序列，并修复关联关系。
    """
    try:
        # 定义项目表与其关联表
        related_tables = [
            {
                "table": "project_tags",
                "fk": "project_id",
                "pk": "tag_id"
            }
        ]
        
        # 重置项目表ID
        result = await reset_table_ids("projects", related_tables)
        
        logger.info("项目ID重置完成")
        return result
    except Exception as e:
        logger.error(f"重置项目ID时出错: {e}")
        return {
            "success": False,
            "message": f"重置项目ID时出错: {e}"
        }


async def fix_database():
    """
    综合数据库修复
    
    执行多项数据库修复操作：
    1. 修复自动递增ID序列
    2. 重置文章ID
    3. 重置标签ID
    4. 重置项目ID
    """
    results = {}
    
    try:
        # 1. 修复自动递增ID序列
        logger.info("开始修复自动递增ID序列...")
        results["fix_autoincrement"] = await fix_autoincrement()
        
        # 2. 重置文章ID
        logger.info("开始重置文章ID...")
        results["reset_article_ids"] = await reset_article_ids()
        
        # 3. 重置标签ID
        logger.info("开始重置标签ID...")
        results["reset_tag_ids"] = await reset_tag_ids()
        
        # 4. 重置项目ID
        logger.info("开始重置项目ID...")
        results["reset_project_ids"] = await reset_project_ids()
        
        return {
            "success": True,
            "message": "数据库修复完成",
            "results": results
        }
    except Exception as e:
        logger.error(f"数据库修复时出错: {e}")
        return {
            "success": False,
            "message": f"数据库修复时出错: {e}",
            "results": results
        }
        

# 如果直接运行此模块，执行数据库修复
if __name__ == "__main__":
    async def main():
        await init_db()
        try:
            await fix_database()
        finally:
            await close_db()
    
    asyncio.run(main()) 