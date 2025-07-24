from tortoise import fields
from tortoise.models import Model


class SkillCategory(Model):
    """
    技能分类模型
    """
    id = fields.IntField(pk=True, description="分类ID，主键")
    name = fields.CharField(max_length=50, description="分类名称")
    icon = fields.CharField(max_length=50, description="分类图标")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")

    class Meta:
        table = "skill_categories"

    def __str__(self):
        return self.name


class Skill(Model):
    """
    技能模型
    """
    id = fields.IntField(pk=True, description="技能ID，主键")
    name = fields.CharField(max_length=50, description="技能名称")
    category = fields.ForeignKeyField(
        "models.SkillCategory", related_name="skills", description="所属分类，外键关联到技能分类"
    )

    class Meta:
        table = "skills"

    def __str__(self):
        return self.name 