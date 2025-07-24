from tortoise import fields
from tortoise.models import Model


class Subscriber(Model):
    """
    订阅者模型
    """
    id = fields.IntField(pk=True, description="订阅者ID，主键")
    email = fields.CharField(max_length=100, unique=True, description="订阅者邮箱，唯一")
    status = fields.CharField(max_length=20, default="active", description="订阅状态，可以是active或unsubscribed")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")

    class Meta:
        table = "subscribers"

    def __str__(self):
        return self.email 