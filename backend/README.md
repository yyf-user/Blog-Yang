# 个人博客系统后端API

这是一个使用FastAPI和Tortoise ORM构建的功能完善的个人博客系统后端，提供全面的API支持，包括文章管理、项目展示、用户认证、API统计等功能。

## 技术栈

- **Web框架**：FastAPI v0.116.1
- **ORM**：Tortoise ORM v0.25.1
- **数据库**：MySQL/SQLite（支持多种数据库后端）
- **认证**：JWT (Python-Jose)，使用Bcrypt进行密码加密
- **文件处理**：Pillow、AioFiles
- **部署**：Uvicorn ASGI服务器

## 快速开始

### 安装

1. 克隆仓库并进入后端目录
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. 创建并激活虚拟环境
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```

3. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

### 配置

本项目使用环境变量进行配置。你可以创建一个`.env`文件在后端目录下，包含以下内容：

```
# 数据库配置
DATABASE_URL=sqlite://./blog.db
# 或者使用MySQL
# DATABASE_URL=mysql://user:password@localhost:3306/blog

# 认证配置
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 跨域配置
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 运行

```bash
# 直接启动
python main.py

# 创建示例数据并启动
python main.py --create-sample-data

# 修复数据库并启动
python main.py --fix-database
```

服务将在 http://127.0.0.1:8000 上启动，API文档在 http://127.0.0.1:8000/docs

## 项目结构详解

```
backend/
├── app/                        # 主应用目录
│   ├── api/                    # API路由
│   │   ├── __init__.py
│   │   ├── api.py              # API路由总集成
│   │   ├── articles.py         # 文章相关API
│   │   ├── auth.py             # 认证相关API
│   │   ├── chat.py             # 聊天功能API
│   │   ├── messages.py         # 消息管理API
│   │   ├── projects.py         # 项目管理API
│   │   ├── skills.py           # 技能管理API
│   │   ├── stats.py            # 统计数据API
│   │   ├── subscribers.py      # 订阅者管理API
│   │   ├── tags.py             # 标签管理API
│   │   ├── uploads.py          # 文件上传API
│   │   └── users.py            # 用户管理API
│   ├── core/                   # 核心配置
│   │   ├── __init__.py
│   │   ├── bcrypt_fix.py       # Bcrypt兼容性修复
│   │   ├── config.py           # 应用配置
│   │   ├── db.py               # 数据库配置
│   │   ├── deps.py             # 依赖项(如获取当前用户)
│   │   ├── security.py         # 安全相关功能
│   │   └── update_stats.py     # 更新统计数据
│   ├── db/                     # 数据库管理
│   │   ├── __init__.py
│   │   ├── base.py             # 模型基类
│   │   ├── database.py         # 数据库连接和操作
│   │   ├── init_db.py          # 数据库初始化
│   │   ├── maintenance.py      # 数据库维护
│   │   └── sample_data.py      # 示例数据生成
│   ├── middleware/             # 中间件
│   │   ├── __init__.py
│   │   └── api_stats_middleware.py # API统计中间件
│   ├── models/                 # 数据模型
│   │   ├── __init__.py
│   │   ├── api_stat.py         # API统计模型
│   │   ├── article.py          # 文章模型
│   │   ├── message.py          # 消息模型
│   │   ├── project.py          # 项目模型
│   │   ├── skill.py            # 技能模型
│   │   ├── stat.py             # 统计数据模型
│   │   ├── subscriber.py       # 订阅者模型
│   │   ├── tag.py              # 标签模型
│   │   └── user.py             # 用户模型
│   ├── schemas/                # 数据架构(Pydantic模型)
│   │   ├── __init__.py
│   │   ├── api_stat.py
│   │   ├── article.py
│   │   ├── message.py
│   │   ├── project.py
│   │   ├── skill.py
│   │   ├── stat.py
│   │   ├── subscriber.py
│   │   ├── tag.py
│   │   ├── token.py
│   │   └── user.py
│   ├── utils/                  # 工具函数
│   │   ├── __init__.py
│   │   ├── database.py         # 数据库工具
│   │   └── slug.py             # 生成友好URL的工具
│   ├── uploads/                # 上传文件目录
│   │   ├── avatars/            # 用户头像
│   │   └── images/             # 其他图片
│   └── main.py                 # 应用入口点
├── scripts/                    # 维护脚本
│   ├── create_api_stats.py     # 创建API统计数据
│   ├── fix_autoincrement.py    # 修复自动递增ID
│   ├── fix_database.py         # 综合数据库修复
│   ├── generate_api_stats.py   # 生成API统计数据
│   ├── reset_article_ids.py    # 重置文章ID
│   └── reset_tag_ids.py        # 重置标签ID
├── static/                     # 静态文件
├── blog.sql                    # 数据库结构SQL
├── main.py                     # 主启动文件
└── requirements.txt            # 依赖项列表
```

## 功能模块详解

### 1. 文章管理

- 创建、更新、删除文章
- 按标签分类文章
- 支持草稿和已发布状态
- 文章封面图片上传
- 阅读统计

相关文件：
- `app/api/articles.py`
- `app/models/article.py`
- `app/schemas/article.py`

### 2. 项目管理

- 管理个人项目展示
- 项目分类与标签
- 项目图片上传
- 项目详情与链接

相关文件：
- `app/api/projects.py`
- `app/models/project.py`
- `app/schemas/project.py`

### 3. 用户认证与管理

- JWT令牌认证
- 用户注册与登录
- 密码哈希保护
- 用户权限控制
- 用户头像上传

相关文件：
- `app/api/auth.py`
- `app/api/users.py`
- `app/core/security.py`
- `app/models/user.py`
- `app/schemas/user.py`
- `app/schemas/token.py`

### 4. API统计

- 自动收集API调用数据
- 响应时间统计
- 错误率统计
- 用户行为分析
- 调用趋势图表

相关文件：
- `app/api/stats.py`
- `app/middleware/api_stats_middleware.py`
- `app/models/api_stat.py`
- `app/schemas/api_stat.py`

### 5. 技能管理

- 个人技能管理
- 技能分类
- 熟练度评估
- 技能展示

相关文件：
- `app/api/skills.py`
- `app/models/skill.py`
- `app/schemas/skill.py`

### 6. 标签系统

- 创建和管理标签
- 为文章和项目添加标签
- 按标签筛选内容

相关文件：
- `app/api/tags.py`
- `app/models/tag.py`
- `app/schemas/tag.py`

### 7. 消息和订阅管理

- 接收用户留言
- 管理电子邮件订阅列表
- 消息通知

相关文件：
- `app/api/messages.py`
- `app/api/subscribers.py`
- `app/models/message.py`
- `app/models/subscriber.py`

### 8. 聊天功能

- 用户与管理员实时聊天
- 消息历史记录
- 未读消息通知

相关文件：
- `app/api/chat.py`
- `app/models/message.py`

### 9. 文件上传

- 支持图片上传
- 头像上传与裁剪
- 文件类型验证
- 安全存储

相关文件：
- `app/api/uploads.py`

## 数据库维护

### 修复ID问题

如果遇到ID不连续或自增问题，可使用以下命令：

```bash
# 修复文章ID
python scripts/reset_article_ids.py

# 修复标签ID
python scripts/reset_tag_ids.py

# 修复所有表的自动递增ID
python scripts/fix_autoincrement.py

# 综合数据库修复
python scripts/fix_database.py
```

### API统计数据

生成模拟的API统计数据：

```bash
# 生成API统计数据
python scripts/generate_api_stats.py

# 或在启动时生成
python main.py --create-sample-data
```

## API文档

系统提供自动生成的API文档：

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 数据库模式

系统使用MySQL/SQLite作为数据库后端，主要表结构包括：

- `users` - 用户信息
- `articles` - 博客文章
- `projects` - 个人项目
- `tags` - 标签系统
- `skills` - 技能管理
- `messages` - 用户留言
- `subscribers` - 电子邮件订阅者
- `api_stats` - API调用统计
- `stats` - 网站统计数据

完整的数据库结构可以在 `blog.sql` 文件中查看。

## 开发指南

### 添加新的API端点

1. 在 `app/api/` 目录下创建或修改相应的路由文件
2. 在 `app/models/` 中添加必要的数据模型
3. 在 `app/schemas/` 中定义请求和响应模式
4. 在 `app/api/api.py` 中注册新的路由器

示例：
```python
# 1. 创建路由文件 app/api/my_feature.py
from fastapi import APIRouter, Depends
from app.core.deps import get_current_user

router = APIRouter()

@router.get("/my-feature")
async def read_my_feature(current_user = Depends(get_current_user)):
    # 实现逻辑
    return {"feature": "data"}

# 2. 在app/api/api.py中注册
from app.api import my_feature

api_router.include_router(
    my_feature.router,
    prefix="/my-feature",
    tags=["my-feature"]
)
```

### 环境配置

本项目使用python-dotenv管理环境变量。创建`.env`文件并配置以下变量：

```
# 数据库配置
DATABASE_URL=sqlite://./blog.db

# JWT配置
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 上传配置
MAX_UPLOAD_SIZE=5242880  # 5MB
ALLOWED_IMAGE_TYPES=image/jpeg,image/png,image/gif

# 其他配置
ENVIRONMENT=development  # development, production
```

## 部署

### 使用Uvicorn

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 使用Gunicorn (生产环境)

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### 使用Docker

```bash
docker build -t blog-backend .
docker run -p 8000:8000 blog-backend
```

## 贡献

欢迎贡献代码、报告问题或提出新功能建议。请遵循以下步骤：

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

本项目采用MIT许可证 - 详情请参阅LICENSE文件 