# 个人博客系统

这是一个功能完善的个人博客系统，分为前端和后端两部分。本项目提供博客文章管理、项目展示、技能标签、用户认证、站内聊天等功能。

## 项目概述

本项目是一个全栈个人博客网站，具有以下主要功能：

- 文章管理：发布、编辑、删除博客文章
- 项目展示：个人项目的展示和详情页
- 用户系统：注册、登录、个人资料管理
- 聊天功能：实时站内聊天
- 后台管理：全面的数据和内容管理系统
- API统计：追踪和分析API使用情况
- 标签系统：对内容进行分类和标记

## 技术栈

### 前端
- **框架**：Vue 3
- **构建工具**：Vite
- **语言**：TypeScript
- **路由**：Vue Router
- **状态管理**：Pinia
- **样式**：CSS/SCSS

### 后端
- **框架**：FastAPI (Python)
- **数据库**：SQL (可能是PostgreSQL或MySQL)
- **认证**：JWT令牌认证
- **ORM**：SQLAlchemy
- **API文档**：Swagger UI (FastAPI内置)

## 目录结构

### 前端结构
```
fronted/blog-fronted/
├── public/                # 静态资源
├── src/
│   ├── api/               # API请求接口
│   ├── assets/            # 静态资源(图片、样式)
│   ├── components/        # Vue组件
│   │   ├── chat/          # 聊天相关组件
│   │   └── icons/         # 图标组件
│   ├── router/            # 路由配置
│   ├── stores/            # 状态管理
│   └── views/             # 页面视图
│       └── admin/         # 管理后台视图
```

### 后端结构
```
backend/
├── app/
│   ├── api/               # API路由和控制器
│   ├── core/              # 核心配置
│   ├── db/                # 数据库相关
│   ├── models/            # 数据模型
│   ├── schemas/           # Pydantic模式
│   └── utils/             # 工具函数
├── scripts/               # 维护脚本
└── venv/                  # Python虚拟环境
```

## 安装与运行

### 前端设置

1. 安装依赖
```sh
cd fronted/blog-fronted
npm install
```

2. 开发环境运行
```sh
npm run dev
```

3. 生产环境构建
```sh
npm run build
```

4. 代码检查
```sh
npm run lint
```

### 后端设置

1. 创建并激活虚拟环境
```sh
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

2. 安装依赖
```sh
pip install -r requirements.txt
```

3. 运行服务器
```sh
python main.py
```

## 主要功能详解

### 博客文章
- 支持Markdown编辑
- 文章分类和标签
- 评论系统

### 项目展示
- 展示个人作品和项目
- 详细的项目描述页面

### 用户系统
- 用户注册和登录
- 个人资料管理
- 权限控制

### 聊天功能
- 实时聊天
- 消息存储和历史记录

### 管理后台
- 文章管理
- 项目管理
- 用户管理
- API统计分析
- 标签管理

## 开发配置

### 推荐的IDE设置

推荐使用[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar)插件(禁用Vetur)进行前端开发。

### TypeScript支持

前端项目使用`vue-tsc`进行类型检查，需要[Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar)插件来支持`.vue`文件的类型。

## 技术文档

- 前端Vite配置参考：[Vite配置文档](https://vitejs.dev/config/)
- Vue 3文档：[Vue 3官方文档](https://v3.vuejs.org/)
- FastAPI文档：[FastAPI官方文档](https://fastapi.tiangolo.com/)

## 作者与贡献

[在此添加作者和贡献者信息]

## 许可证

[在此添加许可证信息]
