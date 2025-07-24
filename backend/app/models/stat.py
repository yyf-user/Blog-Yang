from tortoise import fields
from tortoise.models import Model


class Stat(Model):
    """
    统计数据模型
    """
    id = fields.IntField(pk=True, description="统计ID，主键")
    key = fields.CharField(max_length=50, unique=True, description="统计项键名，唯一")
    value = fields.IntField(description="统计项数值")
    display_text = fields.CharField(max_length=100, description="显示文本")
    updated_at = fields.DatetimeField(auto_now=True, description="最后更新时间")

    class Meta:
        table = "stats"

    def __str__(self):
        return f"{self.key}: {self.value}" 