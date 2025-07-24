from tortoise import fields
from tortoise.models import Model


class Article(Model):
    """
    文章模型
    """
    id = fields.IntField(pk=True, generated=True, description="文章ID，主键，自动生成")
    title = fields.CharField(max_length=255, description="文章标题")
    slug = fields.CharField(max_length=255, unique=True, description="URL友好的标识符，唯一")
    excerpt = fields.TextField(description="文章摘要")
    content = fields.TextField(description="文章正文内容")
    cover_image = fields.CharField(max_length=255, null=True, description="封面图片URL")
    author = fields.ForeignKeyField("models.User", related_name="articles", description="作者，外键关联到用户")
    status = fields.CharField(max_length=20, default="draft", description="文章状态，可以是draft或published")
    featured = fields.BooleanField(default=False, description="是否为推荐文章")
    view_count = fields.IntField(default=0, description="浏览次数")
    read_time = fields.IntField(default=0, description="阅读时间（分钟）")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="最后更新时间")
    published_at = fields.DatetimeField(null=True, description="发布时间")
    tags = fields.ManyToManyField(
        "models.Tag", 
        related_name="articles", 
        through="article_tags",
        forward_key="tag_id",
        backward_key="article_id",
        description="文章标签，多对多关系"
    )

    class Meta:
        table = "articles"

    def __str__(self):
        return self.title


class ArticleTag(Model):
    """
    文章标签关联模型
    """
    article = fields.ForeignKeyField("models.Article", related_name="article_tags", source_field="article_id", description="关联的文章")
    tag = fields.ForeignKeyField("models.Tag", related_name="article_tags", source_field="tag_id", description="关联的标签")

    class Meta:
        table = "article_tags"
        unique_together = (("article", "tag"),) 