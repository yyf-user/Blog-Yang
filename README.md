这是一个功能齐全的个人博客系统，采用前后端分离架构，包括Vue 3前端和FastAPI后端。本项目提供博客文章管理、项目展示、API统计、用户认证、实时聊天等功能。

## 项目概述

本项目是一个专为个人博客/作品集设计的全栈应用，具有以下特点：

- 🚀 **现代化技术栈**：Vue 3 + TypeScript + FastAPI + SQLAlchemy
- 📱 **响应式设计**：适配各种屏幕尺寸的设备
- 🔐 **完善的用户系统**：注册、登录、权限控制
- 📊 **强大的后台管理**：文章、项目、用户、API统计数据管理
- 🔍 **搜索与过滤**：按标签、类别搜索内容
- 💬 **实时聊天功能**：访客与站长直接交流
- 📈 **详细的统计分析**：API调用、用户行为分析

## 系统架构

```
┌─────────────────┐         ┌─────────────────┐
│                 │         │                 │
│     前端        │ ◄─────► │     后端        │
│  Vue 3 + Vite   │   API   │  FastAPI        │
│                 │         │                 │
└─────────────────┘         └─────────────────┘
        │                           │
        │                           │
        ▼                           ▼
┌─────────────────┐         ┌─────────────────┐
│  浏览器缓存/状态 │         │     数据库      │
│  Pinia          │         │  SQLite/MySQL   │
└─────────────────┘         └─────────────────┘
```

## 技术栈详解

### 前端技术栈

- **核心框架**：Vue 3
- **构建工具**：Vite
- **开发语言**：TypeScript
- **路由管理**：Vue Router
- **状态管理**：Pinia
- **HTTP客户端**：Axios
- **UI组件**：自定义组件
- **样式预处理器**：CSS/SCSS

### 后端技术栈

- **Web框架**：FastAPI
- **ORM**：SQLAlchemy/Tortoise ORM
- **数据库**：SQLite/MySQL
- **认证系统**：JWT令牌认证
- **密码加密**：Bcrypt
- **文件处理**：Pillow、AioFiles
- **部署服务器**：Uvicorn (ASGI)

## 目录结构

```
first-project/
├── frontend/                # 前端代码
│   └── blog-frontend/       # Vue 3项目
│       ├── public/          # 静态资源
│       ├── src/             # 源代码
│       │   ├── api/         # API请求
│       │   ├── assets/      # 资源文件
│       │   ├── components/  # Vue组件
│       │   ├── router/      # 路由配置
│       │   ├── stores/      # 状态管理
│       │   └── views/       # 页面视图
│       ├── package.json     # 依赖配置
│       └── vite.config.ts   # Vite配置
│
└── backend/                 # 后端代码
    ├── app/                 # 主应用
    │   ├── api/             # API路由
    │   ├── core/            # 核心配置
    │   ├── db/              # 数据库
    │   ├── middleware/      # 中间件
    │   ├── models/          # 数据模型
    │   ├── schemas/         # 数据架构
    │   └── utils/           # 工具函数
    ├── scripts/             # 实用脚本
    ├── main.py              # 入口文件
    └── requirements.txt     # 依赖项
```
### 首页效果图片
<img width="1401" height="955" alt="屏幕截图 2025-10-02 112006" src="https://github.com/user-attachments/assets/f4b2ce0d-d2ef-42d5-924f-79dae48eae60" />

### 内容页面图片
<img width="1800" height="962" alt="屏幕截图 2025-10-02 112026" src="https://github.com/user-attachments/assets/932bcc7b-f59c-4905-904f-f85e8fe33607" />

### 后台管理页面图片
<img width="1915" height="956" alt="屏幕截图 2025-10-02 112037" src="https://github.com/user-attachments/assets/c80b79ca-aa2c-4088-b5a9-139891e97f31" />

## 核心功能

### 1. 博客文章系统

- 支持Markdown编辑器
- 文章分类与标签
- 草稿与发布状态
- 阅读时间估算
- 文章封面图片上传
- 阅读量统计

### 2. 项目展示

- 项目列表与详情页
- 项目分类与标签
- 项目图片展示
- 外部链接支持
- 技术栈标签

### 3. 用户管理系统

- 注册与登录
- JWT令牌认证
- 用户角色与权限
- 个人资料管理
- 头像上传与裁剪

### 4. 聊天功能

- 实时聊天
- 未读消息提醒
- 消息历史记录
- 在线状态显示

### 5. API统计分析

- API调用记录
- 响应时间统计
- 错误率分析
- 用户行为追踪
- 可视化统计图表

### 6. 订阅与消息管理

- 邮件订阅列表
- 访客留言管理
- 消息状态跟踪

## 安装与运行

### 环境要求

- Node.js 18+
- Python 3.10+
- MySQL/SQLite

### 前端设置

```bash
# 进入前端目录
cd frontend/blog-frontend

# 安装依赖
npm install

# 开发环境运行
npm run dev

# 构建生产版本
npm run build
```

### 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate
# 或 (Linux/Mac)
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
python main.py
```

## 配置指南

### 前端配置

创建 `frontend/blog-frontend/.env.local` 文件：

```
VITE_API_URL=http://localhost:8000/api
VITE_ASSETS_URL=http://localhost:8000/static
```

### 后端配置

创建 `backend/.env` 文件：

```
# 数据库配置
DATABASE_URL=sqlite://./blog.db
# 或使用MySQL
# DATABASE_URL=mysql://user:password@localhost:3306/blog

# 认证配置
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 跨域配置
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

## 开发指南

### 前端开发

1. **添加新页面**
   - 在 `src/views` 创建Vue组件
   - 在 `src/router/index.ts` 添加路由配置

2. **添加新API请求**
   - 在 `src/api/index.ts` 添加API请求函数

3. **添加新状态**
   - 在 `src/stores` 创建新的Pinia存储

### 后端开发

1. **添加新的API端点**
   - 在 `app/api/` 创建或修改路由文件
   - 在 `app/api/api.py` 注册路由

2. **创建新的数据模型**
   - 在 `app/models/` 添加模型类
   - 在 `app/schemas/` 添加对应的数据架构

3. **数据库迁移**
   - 使用脚本更新数据库结构

## 部署指南

### 前端部署

1. **构建生产版本**
   ```bash
   cd frontend/blog-frontend
   npm run build
   ```

2. **部署静态文件**
   - 将 `dist` 目录部署到Nginx或其他Web服务器

### 后端部署

1. **使用Uvicorn**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

2. **使用Gunicorn (生产环境)**
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
   ```

3. **使用Docker**
   ```bash
   docker build -t blog-backend .
   docker run -p 8000:8000 blog-backend
   ```

## API文档

后端提供自动生成的API文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 主要功能详情

### 文章管理

- 支持文章创建、编辑、删除
- 可设置文章状态（草稿/已发布）
- 支持标签和分类
- 文章统计信息（阅读量、发布时间）
- 封面图片上传

### 项目管理

- 项目展示（标题、描述、图片）
- 项目分类和标签
- 项目链接（GitHub、演示链接）
- 技术栈标签

### 用户系统

- 用户注册和登录
- 基于JWT的身份验证
- 用户角色和权限控制
- 个人资料管理
- 头像上传和编辑

### 聊天系统

- 实时消息发送和接收
- 消息存储和历史记录
- 未读消息通知

### 后台统计

- API调用统计
- 用户活动分析
- 错误率和性能指标
- 可视化数据展示

## 贡献指南

欢迎贡献代码、报告问题或提出新功能建议！请遵循以下步骤：

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

本项目采用MIT许可证 - 详情请参阅LICENSE文件

## 作者

[Yangyf]

## 致谢

感谢所有开源项目和贡献者，他们的工作使得本项目成为可能。 
