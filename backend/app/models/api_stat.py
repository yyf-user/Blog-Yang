from tortoise import fields
from tortoise.models import Model
from datetime import datetime


class ApiStat(Model):
    """
    API调用统计数据模型
    """
    id = fields.IntField(pk=True, description="统计ID，主键")
    endpoint = fields.CharField(max_length=255, description="API路径")
    method = fields.CharField(max_length=10, description="HTTP方法，如GET、POST等")
    status_code = fields.IntField(description="HTTP状态码")
    response_time = fields.FloatField(description="响应时间(秒)")
    timestamp = fields.DatetimeField(description="调用时间")
    user_id = fields.IntField(null=True, description="用户ID，可为空表示匿名访问")

    class Meta:
        table = "api_stat"

    def __str__(self):
        return f"{self.method} {self.endpoint}: {self.status_code}"
    
    @property
    def is_error(self):
        """判断是否为错误请求"""
        return self.status_code >= 400


class ApiStatDaily(Model):
    """
    API调用每日统计数据模型
    """
    id = fields.IntField(pk=True, description="每日统计ID，主键")
    date = fields.DateField(description="统计日期")
    total_calls = fields.IntField(default=0, description="当日API总调用次数")
    unique_users = fields.IntField(default=0, description="当日独立用户数")
    avg_response_time = fields.FloatField(default=0, description="当日平均响应时间(毫秒)")
    error_count = fields.IntField(default=0, description="当日错误请求次数")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="最后更新时间")

    class Meta:
        table = "api_stats_daily"
        unique_together = (("date",),)

    def __str__(self):
        return f"{self.date}: {self.total_calls} calls"
    
    @property
    def error_rate(self):
        """计算错误率"""
        if self.total_calls == 0:
            return 0
        return round((self.error_count / self.total_calls) * 100, 1)


class ApiStatusCode(Model):
    """
    API状态码统计数据模型
    """
    id = fields.IntField(pk=True, description="状态码统计ID，主键")
    api_stat = fields.ForeignKeyField('models.ApiStat', related_name='status_codes', description="关联的API统计记录")
    status_code = fields.IntField(description="HTTP状态码")
    count = fields.IntField(default=0, description="该状态码出现次数")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="最后更新时间")

    class Meta:
        table = "api_status_codes"
        unique_together = (("api_stat_id", "status_code"),)

    def __str__(self):
        return f"{self.api_stat.method} {self.api_stat.endpoint} - {self.status_code}: {self.count}" 