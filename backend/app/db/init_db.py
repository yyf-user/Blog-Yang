"""
数据库初始化模块

提供初始化数据和创建初始超级用户的功能
"""
import logging
from app.core.config import settings
from app.models.user import User

logger = logging.getLogger(__name__)


async def create_first_superuser() -> None:
    """
    创建初始超级用户
    
    如果不存在具有配置文件中指定用户名的超级用户，
    则创建一个新的超级用户。
    """
    user = await User.filter(username=settings.FIRST_SUPERUSER).first()
    if not user:
        user_obj = User(
            username=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER_EMAIL,
            full_name="管理员",
            role="admin",
        )
        await user_obj.set_password(settings.FIRST_SUPERUSER_PASSWORD)
        await user_obj.save()
        logger.info(f"初始超级用户 {settings.FIRST_SUPERUSER} 已创建")
    else:
        logger.info(f"超级用户 {settings.FIRST_SUPERUSER} 已存在，跳过创建")


async def init_db() -> None:
    """
    初始化数据库
    
    此函数已移至 app.db.database 模块。
    保留此函数以保持向后兼容性。
    """
    from app.db.database import init_db as _init_db
    await _init_db() 