"""
数据库访问模块

提供数据库连接、事务处理和通用查询操作
"""
import logging
from typing import Any, Dict, List, Optional, Type, TypeVar
from tortoise import Tortoise, connections
from tortoise.models import Model
from tortoise.transactions import in_transaction
from tortoise.exceptions import DoesNotExist, OperationalError

from app.core.config import settings

logger = logging.getLogger(__name__)

# 定义模型类型变量
T = TypeVar('T', bound=Model)


# 重新导出Tortoise ORM的事务函数
transaction = in_transaction


async def init_db() -> None:
    """
    初始化数据库连接和模型
    
    如果使用SQLite：
    - 直接连接到SQLite数据库文件
    - 生成数据库架构
    
    如果使用MySQL：
    - 先连接到MySQL服务器，不指定数据库
    - 检查并创建数据库（如果不存在）
    - 重新连接到指定的数据库
    - 生成数据库架构
    """
    try:
        # 判断使用的是哪种数据库
        if settings.DATABASE_URL.startswith('sqlite'):
            # SQLite数据库
            await Tortoise.init(
                db_url=settings.DATABASE_URL,
                modules={"models": ["app.models"]},
            )
            
            # 生成数据库架构（使用safe=True，不会删除已有的表和数据）
            await Tortoise.generate_schemas(safe=True)
            logger.info("SQLite数据库架构已检查/更新")
            
        else:
            # MySQL数据库
            # 先连接到MySQL服务器，不指定数据库
            mysql_url = settings.DATABASE_URL.rsplit('/', 1)[0]
            db_name = settings.DATABASE_URL.rsplit('/', 1)[1]
            
            # 初始化Tortoise连接到MySQL服务器
            await Tortoise.init(
                db_url=mysql_url,
                modules={"models": ["app.models"]},
            )
            
            # 获取数据库连接
            connection = connections.get("default")
            
            # 检查数据库是否存在
            result = await connection.execute_query(f"SHOW DATABASES LIKE '{db_name}'")
            db_exists = len(result[1]) > 0
            
            if not db_exists:
                # 如果数据库不存在，创建它
                try:
                    await connection.execute_query(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                    logger.info(f"数据库 {db_name} 不存在，已创建")
                except Exception as e:
                    logger.error(f"创建数据库时出错: {e}")
                    raise
            else:
                logger.info(f"数据库 {db_name} 已存在，跳过创建")
            
            # 关闭当前连接
            await Tortoise.close_connections()
            
            # 重新连接到指定的数据库
            await Tortoise.init(
                db_url=settings.DATABASE_URL,
                modules={"models": ["app.models"]},
            )
            
            # 生成数据库架构（使用safe=True，不会删除已有的表和数据）
            await Tortoise.generate_schemas(safe=True)
            logger.info("MySQL数据库架构已检查/更新")
        
        # 创建超级用户（如果不存在）
        from app.db.init_db import create_first_superuser
        await create_first_superuser()
        
        logger.info("数据库初始化完成")
        
    except Exception as e:
        logger.error(f"初始化数据库时出错: {e}")
        raise


async def close_db() -> None:
    """关闭数据库连接"""
    await Tortoise.close_connections()
    logger.info("数据库连接已关闭")


async def execute_query(query: str, params: Optional[List[Any]] = None) -> Dict[str, Any]:
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


async def fix_sequence(table_name: str) -> None:
    """
    修复SQLite自动递增序列
    
    Args:
        table_name: 表名
    """
    try:
        if settings.DATABASE_URL.startswith('sqlite'):
            # 获取当前最大ID
            query = f"SELECT MAX(id) as max_id FROM {table_name}"
            result = await execute_query(query)
            max_id = result["results"][0]["max_id"] or 0
            
            # 更新sqlite_sequence表
            await execute_query(
                "INSERT OR REPLACE INTO sqlite_sequence (name, seq) VALUES (?, ?)",
                [table_name, max_id]
            )
            logger.info(f"已修复表 {table_name} 的自动递增序列，设置为 {max_id}")
        else:
            logger.info(f"当前数据库不是SQLite，跳过修复自动递增序列")
    except Exception as e:
        logger.error(f"修复自动递增序列时出错: {e}")
        raise


async def get_by_id(model_class: Type[T], id: int) -> Optional[T]:
    """
    通过ID获取模型实例
    
    Args:
        model_class: 模型类
        id: 实例ID
        
    Returns:
        模型实例，如果不存在则返回None
    """
    try:
        return await model_class.get(id=id)
    except DoesNotExist:
        return None 