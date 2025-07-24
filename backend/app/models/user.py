from tortoise import fields
from tortoise.models import Model

from app.core.security import get_password_hash, verify_password


class User(Model):
    """
    用户模型
    """
    id = fields.IntField(pk=True, description="用户ID，主键")
    username = fields.CharField(max_length=50, unique=True, description="用户名，唯一")
    email = fields.CharField(max_length=100, unique=True, description="电子邮箱，唯一")
    password_hash = fields.CharField(max_length=255, description="密码哈希值")
    full_name = fields.CharField(max_length=100, null=True, description="用户全名")
    bio = fields.TextField(null=True, description="个人简介")
    avatar_url = fields.CharField(max_length=255, null=True, description="头像URL地址")
    role = fields.CharField(max_length=20, default="user", description="用户角色，可以是admin或user")
    github_url = fields.CharField(max_length=255, null=True, description="GitHub主页地址")
    linkedin_url = fields.CharField(max_length=255, null=True, description="LinkedIn主页地址")
    twitter_url = fields.CharField(max_length=255, null=True, description="Twitter主页地址")
    website_url = fields.CharField(max_length=255, null=True, description="个人网站地址")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="最后更新时间")

    class Meta:
        table = "users"

    def __str__(self):
        return self.username

    async def set_password(self, password: str) -> None:
        """设置密码"""
        self.password_hash = get_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """验证密码"""
        return verify_password(password, self.password_hash) 