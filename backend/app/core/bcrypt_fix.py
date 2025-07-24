"""
修复 bcrypt 和 passlib 之间的兼容性问题
"""
import logging
import bcrypt

logger = logging.getLogger(__name__)

# 为 bcrypt 添加缺失的 __about__ 属性
if not hasattr(bcrypt, "__about__"):
    try:
        # 尝试获取版本信息
        version = bcrypt.__version__
        
        # 创建一个模拟的 __about__ 模块
        class About:
            __version__ = version
        
        bcrypt.__about__ = About()
        logger.info(f"已为 bcrypt 添加 __about__ 属性，版本: {version}")
    except Exception as e:
        logger.warning(f"无法为 bcrypt 添加 __about__ 属性: {e}") 