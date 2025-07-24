"""
主应用模块

此模块包含FastAPI应用的入口点，
负责创建应用实例、注册路由和中间件、初始化数据库等。
"""
import os
import sys
import logging
import time
from pathlib import Path
from contextlib import asynccontextmanager

# 添加项目根目录到Python路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.api import api_router
from app.core.config import settings
from app.middleware.api_stats_middleware import ApiStatsMiddleware

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# 设置第三方库的日志级别为WARNING，减少不必要的日志输出
logging.getLogger("tortoise").setLevel(logging.WARNING)
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("aiomysql").setLevel(logging.WARNING)

logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期事件处理器
    
    在应用启动时执行初始化操作，在应用关闭时执行清理操作
    """
    # 启动时执行
    logger.info("应用启动中...")
    
    try:
        # 创建初始超级用户
        from app.db.init_db import create_first_superuser
        await create_first_superuser()
        
        # 更新统计数据
        from app.api.stats import update_all_stats
        await update_all_stats()
    except Exception as e:
        logger.error(f"初始化过程中出错: {e}")
    
    logger.info("应用初始化完成")
    
    yield  # 这里是应用运行的部分
    
    # 关闭时执行
    logger.info("应用关闭中...")
    
    # 关闭数据库连接
    from tortoise import Tortoise
    await Tortoise.close_connections()
    
    logger.info("应用已安全关闭")


def create_app() -> FastAPI:
    """创建FastAPI应用实例"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan,  # 使用新的lifespan事件处理器
    )
    
    # 设置CORS - 先清除所有中间件，确保没有重复的CORS中间件
    app.middleware_stack = None
    app.build_middleware_stack()
    
    # 添加CORS中间件（不输出日志）
    origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["Content-Type", "Authorization"],
        max_age=600,
    )
    
    # 添加API统计中间件
    app.add_middleware(ApiStatsMiddleware)
    
    # 请求日志中间件 - 只记录API请求
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        # 只记录API请求
        is_api_request = request.url.path.startswith("/api/")
        start_time = time.time()
        response = await call_next(request)
        
        if is_api_request:
            process_time = time.time() - start_time
            logger.info(f"API请求: {request.method} {request.url.path} - 状态码: {response.status_code} - 处理时间: {process_time:.4f}秒")
        
        return response
    
    # 添加API路由
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    # 添加静态文件服务
    if not os.path.exists(settings.UPLOAD_DIR):
        os.makedirs(settings.UPLOAD_DIR)
    
    # 获取当前文件的目录
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(base_dir, "static")
    
    # 确保静态目录存在
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    @app.get("/")
    def root():
        """根路径响应"""
        return {"message": "欢迎使用博客Yang-API"}
    
    # 注册Tortoise ORM
    from tortoise.contrib.fastapi import register_tortoise
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    
    return app


app = create_app()

# 如果直接运行此文件，则启动Uvicorn服务器
if __name__ == "__main__":
    import uvicorn
    import asyncio
    
    # 启动图案
    STARTUP_BANNER = r"""
   _____          _   _ _____  _____ _____ 
 |  ___|_ _  ___| |_(_)  ___|| ____|_   _|
 | |_ / _` |/ __| __| | |_   |  _|   | |  
 |  _| (_| | (__| |_| |  _|  | |___  | |  
 |_|  \__,_|\___|\__|_|_|    |_____| |_|  
  ::    F A S T A P I    ::    (v1.0.0)
"""
    print(STARTUP_BANNER)
    
    # 启动服务器
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="error"  # 设置uvicorn日志级别为error，减少输出
    )