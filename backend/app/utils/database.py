"""
数据库实用工具模块

此模块提供各种数据库操作的辅助函数，
如重置ID序列、批量操作等。
"""

import logging
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from tortoise.models import Model
from tortoise.transactions import in_transaction

# 修复导入路径
from tortoise import connections

from app.core.config import settings

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=Model)


async def reset_table_ids(
    table_name: str, 
    related_tables: Optional[List[Dict[str, str]]] = None
) -> None:
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
    """
    if not settings.DATABASE_URL.startswith('sqlite'):
        logger.warning("重置ID序列仅支持SQLite数据库")
        return
    
    db_path = Path(settings.DATABASE_URL.replace("sqlite://", ""))
    
    if not db_path.exists():
        logger.error(f"数据库文件不存在: {db_path}")
        return
    
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
        
    except Exception as e:
        conn.rollback()
        logger.error(f"重置表 {table_name} 的ID时出错: {e}")
        raise
    finally:
        conn.close()


async def bulk_create(model_class: Type[T], data: List[Dict[str, Any]]) -> List[T]:
    """
    批量创建模型实例
    
    Args:
        model_class: 模型类
        data: 包含模型数据的字典列表
        
    Returns:
        创建的模型实例列表
    """
    instances = []
    async with in_transaction():
        for item in data:
            instance = model_class(**item)
            await instance.save()
            instances.append(instance)
    return instances


async def bulk_update(
    model_class: Type[T], 
    data: List[Dict[str, Any]], 
    id_field: str = "id"
) -> List[T]:
    """
    批量更新模型实例
    
    Args:
        model_class: 模型类
        data: 包含模型数据的字典列表，每个字典必须包含id_field指定的字段
        id_field: 标识模型实例的字段名，默认为"id"
        
    Returns:
        更新的模型实例列表
    """
    instances = []
    async with in_transaction():
        for item in data:
            if id_field not in item:
                logger.warning(f"跳过没有 {id_field} 字段的项: {item}")
                continue
                
            instance = await model_class.filter(**{id_field: item[id_field]}).first()
            if not instance:
                logger.warning(f"找不到 {id_field}={item[id_field]} 的实例")
                continue
                
            # 更新实例
            for key, value in item.items():
                if key != id_field:
                    setattr(instance, key, value)
                    
            await instance.save()
            instances.append(instance)
            
    return instances


async def execute_raw_query(query: str, params: Optional[List[Any]] = None) -> Dict[str, Any]:
    """
    执行原始SQL查询
    
    Args:
        query: SQL查询语句
        params: 查询参数
        
    Returns:
        查询结果
    """
    try:
        connection = connections.get("default")
        result = await connection.execute_query(query, params or [])
        return {
            "rows_affected": result[0],
            "results": result[1]
        }
    except Exception as e:
        logger.error(f"执行查询时出错: {e}, 查询: {query}, 参数: {params}")
        raise 