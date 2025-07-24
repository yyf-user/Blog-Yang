import time
from datetime import datetime, date
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import logging
from tortoise.exceptions import DoesNotExist, OperationalError

from app.models.api_stat import ApiStat, ApiStatDaily, ApiStatusCode
from app.db import transaction

logger = logging.getLogger(__name__)


class ApiStatsMiddleware(BaseHTTPMiddleware):
    """
    中间件，用于记录API调用统计信息
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # 记录请求开始时间
        start_time = time.time()
        
        # 获取请求路径和方法
        path = request.url.path
        method = request.method
        
        # 只记录API请求
        is_api_request = path.startswith("/api/")
        
        # 调用下一个中间件或路由处理函数
        response = await call_next(request)
        
        # 如果不是API请求，直接返回
        if not is_api_request:
            return response
        
        # 计算处理时间
        process_time = time.time() - start_time
        
        # 记录API调用统计
        try:
            user_id = None
            # 尝试从请求中获取用户ID (不同的方式)
            # 1. 从请求状态中获取
            if hasattr(request.state, "user") and request.state.user:
                user_id = request.state.user.id
            
            # 2. 从请求头中获取认证信息
            auth_header = request.headers.get("Authorization")
            if not user_id and auth_header and auth_header.startswith("Bearer "):
                # 尝试解析JWT令牌，这里简化处理
                # 在实际实现中，你可能需要解析JWT令牌并获取用户ID
                try:
                    from app.core.security import decode_jwt_token
                    token = auth_header.replace("Bearer ", "")
                    payload = decode_jwt_token(token)
                    if payload and "sub" in payload:
                        user_id = int(payload["sub"])
                except Exception as e:
                    logger.error(f"解析JWT令牌失败: {e}")
            
            # 规范化路径，将ID部分替换为{id}，以便统计相同API
            normalized_path = self._normalize_path(path)
            
            # 使用事务确保数据一致性
            async with transaction() as conn:
                # 记录单次API调用
                try:
                    api_stat = await ApiStat.create(
                        endpoint=normalized_path,  # 使用规范化的路径
                        method=method,
                        status_code=response.status_code,
                        response_time=process_time,
                        timestamp=datetime.now(),
                        user_id=user_id
                    )
                    
                    # 更新每日统计
                    await self._update_daily_stats(process_time, response.status_code)
                    
                    # 记录详细日志
                    logger.debug(
                        f"API调用: {method} {normalized_path} - 状态码: {response.status_code} - "
                        f"响应时间: {process_time:.4f}秒 - 用户ID: {user_id or '匿名'}"
                    )
                except OperationalError as e:
                    logger.error(f"数据库操作错误: {e}")
                    # 可能是表不存在，忽略错误
                    pass
            
        except Exception as e:
            logger.error(f"记录API统计信息失败: {e}")
        
        return response
    
    def _normalize_path(self, path: str) -> str:
        """
        规范化API路径，将数字ID替换为{id}，以便统计相同API
        例如: /api/articles/123 -> /api/articles/{id}
        """
        import re
        # 匹配URL中的数字部分
        normalized = re.sub(r'/(\d+)(?:/|$)', '/{id}/', path)
        # 确保路径不以/结尾
        if normalized.endswith('/') and len(normalized) > 1:
            normalized = normalized[:-1]
        return normalized
    
    async def _update_daily_stats(self, process_time: float, status_code: int) -> None:
        """
        更新每日统计
        """
        try:
            # 获取今天的日期
            today = date.today()
            
            # 尝试获取今天的统计
            daily_stat = await ApiStatDaily.filter(date=today).first()
            
            # 如果不存在，创建新的
            if not daily_stat:
                daily_stat = await ApiStatDaily.create(
                    date=today,
                    total_calls=0,
                    unique_users=0,
                    avg_response_time=0,
                    error_count=0
                )
            
            # 更新调用次数
            daily_stat.total_calls += 1
            
            # 更新平均响应时间
            daily_stat.avg_response_time = ((daily_stat.avg_response_time * (daily_stat.total_calls - 1)) + (process_time * 1000)) / daily_stat.total_calls
            
            # 如果是错误状态码，增加错误计数
            if status_code >= 400:
                daily_stat.error_count += 1
            
            # 保存每日统计
            await daily_stat.save()
            
            # 每天收集的独立用户数更新
            # 我们使用定时任务来更新这个值，而不是每次API调用都更新
            # 可以通过 app.core.update_stats 中的 update_visitor_count 函数来实现
        except Exception as e:
            logger.error(f"更新每日统计失败: {e}") 