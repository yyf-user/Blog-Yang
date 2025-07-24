import asyncio
import logging
import os
import sys

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from tortoise import Tortoise, connections
from app.core.config import settings

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("database_fix")

async def fix_database():
    """修复数据库中的article_tags表"""
    # 使用项目配置中的数据库URL
    db_url = settings.DATABASE_URL
    
    try:
        # 初始化Tortoise ORM
        logger.info(f"正在连接到数据库: {db_url}")
        await Tortoise.init(
            db_url=db_url,
            modules={"models": [
                "app.models.article", 
                "app.models.tag",
                "app.models.user",
                "app.models.project",
                "app.models.message",
                "app.models.skill",
                "app.models.stat",
                "app.models.api_stat",
                "app.models.subscriber"
            ]},
        )
        
        logger.info("获取数据库连接...")
        connection = connections.get("default")
        
        # 检查article_tags表是否存在
        logger.info("检查article_tags表...")
        result = await connection.execute_query("SHOW TABLES LIKE 'article_tags'")
        table_exists = len(result[1]) > 0
        
        if table_exists:
            # 查看表结构
            logger.info("查看article_tags表结构...")
            columns = await connection.execute_query("DESCRIBE article_tags")
            logger.info(f"表结构: {columns[1]}")
            
            # 删除已存在的表
            logger.info("正在删除现有的article_tags表...")
            await connection.execute_query("DROP TABLE article_tags")
            logger.info("article_tags表已删除")
        
        # 检查 ApiStat 表是否存在
        result = await connection.execute_query("SHOW TABLES LIKE 'api_stat'")
        api_stat_exists = len(result[1]) > 0
        
        if not api_stat_exists:
            logger.info("创建api_stat表...")
            await connection.execute_query("""
                CREATE TABLE `api_stat` (
                  `id` INT NOT NULL AUTO_INCREMENT,
                  `endpoint` VARCHAR(255) NOT NULL,
                  `method` VARCHAR(10) NOT NULL,
                  `status_code` INT NOT NULL,
                  `response_time` DOUBLE NOT NULL,
                  `timestamp` DATETIME(6) NOT NULL,
                  `user_id` INT,
                  PRIMARY KEY (`id`),
                  INDEX `idx_api_stat_endpoint` (`endpoint`),
                  INDEX `idx_api_stat_timestamp` (`timestamp`),
                  INDEX `idx_api_stat_user_id` (`user_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)
            logger.info("api_stat表已创建")
        
        # 重新生成架构 - 这将创建具有正确列名的新表
        logger.info("重新生成数据库架构...")
        await Tortoise.generate_schemas(safe=True)
        logger.info("数据库架构已更新")
        
        logger.info("修复完成！")
    except Exception as e:
        logger.error(f"修复数据库时出错: {e}")
        raise
    finally:
        # 关闭数据库连接
        await Tortoise.close_connections()

if __name__ == "__main__":
    try:
        logger.info("开始修复数据库...")
        asyncio.run(fix_database())
        logger.info("数据库修复完成！")
    except Exception as e:
        logger.error(f"数据库修复失败: {e}")
        sys.exit(1) 