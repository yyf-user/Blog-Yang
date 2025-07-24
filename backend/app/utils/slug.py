import re
from slugify import slugify


def generate_slug(text: str) -> str:
    """
    生成URL友好的slug
    """
    return slugify(text)


def generate_username_slug(username: str) -> str:
    """
    生成用户名的slug
    """
    # 移除非字母数字字符
    clean_username = re.sub(r'[^\w\s]', '', username)
    # 转换为小写并替换空格为连字符
    return clean_username.lower().replace(' ', '-') 