from tortoise import fields
from tortoise.models import Model


class Project(Model):
    """
    项目模型
    """
    id = fields.IntField(pk=True, generated=True, description="项目ID，主键，自动生成")
    title = fields.CharField(max_length=255, description="项目标题")
    slug = fields.CharField(max_length=255, unique=True, description="URL友好的标识符，唯一")
    description = fields.TextField(description="项目描述")
    image_url = fields.CharField(max_length=255, null=True, description="项目图片URL")
    github_url = fields.CharField(max_length=255, null=True, description="GitHub仓库地址")
    live_url = fields.CharField(max_length=255, null=True, description="项目线上地址")
    featured = fields.BooleanField(default=False, description="是否为推荐项目")
    stars_count = fields.IntField(default=0, description="GitHub星标数量")
    forks_count = fields.IntField(default=0, description="GitHub分支数量")
    emoji = fields.CharField(max_length=10, null=True, description="项目emoji图标")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="最后更新时间")
    tags = fields.ManyToManyField(
        "models.Tag", related_name="projects", through="project_tags",
        description="项目标签，多对多关系"
    )

    class Meta:
        table = "projects"

    def __str__(self):
        return self.title


class ProjectTag(Model):
    """
    项目标签关联模型
    """
    project = fields.ForeignKeyField("models.Project", related_name="project_tags", description="关联的项目")
    tag = fields.ForeignKeyField("models.Tag", related_name="project_tags", description="关联的标签")

    class Meta:
        table = "project_tags"
        unique_together = (("project_id", "tag_id"),) 