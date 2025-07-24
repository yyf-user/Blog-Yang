from tortoise import fields
from tortoise.models import Model


class Message(Model):
    """
    联系消息模型
    """
    id = fields.IntField(pk=True, generated=True, description="消息ID，主键，自动生成")
    name = fields.CharField(max_length=100, description="发送者姓名")
    email = fields.CharField(max_length=100, description="发送者邮箱")
    subject = fields.CharField(max_length=255, description="消息主题")
    message = fields.TextField(description="消息内容")
    is_read = fields.BooleanField(default=False, description="是否已读")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")

    class Meta:
        table = "messages"

    def __str__(self):
        return self.subject 