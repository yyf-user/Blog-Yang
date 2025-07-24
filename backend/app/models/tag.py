from tortoise import fields
from tortoise.models import Model


class Tag(Model):
    """
    标签模型
    """
    id = fields.IntField(pk=True, generated=True, description="标签ID，主键，自动生成")
    name = fields.CharField(max_length=50, unique=True, description="标签名称，唯一")
    slug = fields.CharField(max_length=50, unique=True, description="URL友好的标识符，唯一")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")

    class Meta:
        table = "tags"

    def __str__(self):
        return self.name 