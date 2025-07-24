"""
样本数据生成模块

提供各种样本数据生成功能，用于开发和测试环境。
"""

import random
import logging
import asyncio
from datetime import datetime, timedelta, date
from typing import Dict, List, Any, Optional

from app.db import transaction, init_db, close_db
from app.models.api_stat import ApiStat, ApiStatDaily
from app.core.config import settings

logger = logging.getLogger(__name__)


async def generate_api_stats(days: int = 7, min_calls_per_day: int = 50, max_calls_per_day: int = 150):
    """
    生成API统计样本数据
    
    Args:
        days: 生成多少天的数据
        min_calls_per_day: 每天最少调用次数
        max_calls_per_day: 每天最多调用次数
        
    Returns:
        统计信息字典
    """
    logger.info("开始生成API统计样本数据...")
    
    # 清除现有API统计数据
    await ApiStat.all().delete()
    await ApiStatDaily.all().delete()
    
    # 生成过去n天的数据
    today = datetime.now()
    
    # 创建API端点列表
    endpoints = [
        {"path": "/api/articles", "method": "GET"},
        {"path": "/api/articles/{id}", "method": "GET"},
        {"path": "/api/articles", "method": "POST"},
        {"path": "/api/articles/{id}", "method": "PUT"},
        {"path": "/api/articles/{id}", "method": "DELETE"},
        {"path": "/api/tags", "method": "GET"},
        {"path": "/api/tags", "method": "POST"},
        {"path": "/api/projects", "method": "GET"},
        {"path": "/api/auth/login", "method": "POST"},
        {"path": "/api/users/me", "method": "GET"},
        {"path": "/api/stats/api", "method": "GET"},
        {"path": "/api/messages", "method": "GET"},
        {"path": "/api/messages", "method": "POST"},
        {"path": "/api/uploads/image", "method": "POST"},
    ]
    
    # 创建用户ID列表
    user_ids = [1, 2, 3, 4, 5, None]  # None 表示匿名用户
    
    total_calls = 0
    daily_stats = []
    
    # 生成每天的统计数据
    for day_offset in range(days):
        current_date = today - timedelta(days=day_offset)
        day_start = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # 为这一天生成的API调用次数
        # 越近的日期调用次数越多
        daily_calls = random.randint(min_calls_per_day, max_calls_per_day) + (days - day_offset) * 10
        
        # 今天的独立用户数
        unique_users_count = 0
        users_seen = set()
        
        # 今天的错误请求数
        error_count = 0
        
        # 今天的总响应时间
        total_response_time = 0
        
        logger.info(f"为 {current_date.date()} 生成 {daily_calls} 条API调用记录...")
        
        # 生成当天的API调用记录
        for i in range(daily_calls):
            # 随机选择一个API端点
            endpoint = random.choice(endpoints)
            
            # 随机选择一个用户ID
            user_id = random.choice(user_ids)
            if user_id is not None:
                users_seen.add(user_id)
            
            # 生成随机时间
            hours = random.randint(0, 23)
            minutes = random.randint(0, 59)
            seconds = random.randint(0, 59)
            timestamp = current_date.replace(
                hour=hours, minute=minutes, second=seconds, microsecond=random.randint(0, 999999)
            )
            
            # 生成随机响应时间（20-500毫秒）
            response_time = random.uniform(0.02, 0.5)
            total_response_time += response_time
            
            # 生成随机状态码，大部分成功，少部分失败
            status_code = 200
            if random.random() < 0.05:  # 5%的错误率
                error_status_codes = [400, 401, 403, 404, 500]
                status_code = random.choice(error_status_codes)
                error_count += 1
            
            # 创建API调用记录
            await ApiStat.create(
                endpoint=endpoint["path"],
                method=endpoint["method"],
                status_code=status_code,
                response_time=response_time,
                timestamp=timestamp,
                user_id=user_id
            )
            
        # 更新总调用次数
        total_calls += daily_calls
        
        # 计算今天的独立用户数
        unique_users_count = len(users_seen)
        
        # 计算今天的平均响应时间
        avg_response_time = (total_response_time / daily_calls) * 1000  # 转换为毫秒
        
        # 创建每日统计数据
        daily_stat = await ApiStatDaily.create(
            date=current_date.date(),
            total_calls=daily_calls,
            unique_users=unique_users_count,
            avg_response_time=avg_response_time,
            error_count=error_count
        )
        
        daily_stats.append({
            "date": current_date.date().isoformat(),
            "total_calls": daily_calls,
            "unique_users": unique_users_count,
            "avg_response_time": round(avg_response_time, 2),
            "error_count": error_count,
            "error_rate": round((error_count / daily_calls) * 100, 1) if daily_calls > 0 else 0
        })
    
    logger.info(f"API统计样本数据生成完成! 总共生成了 {total_calls} 条API调用记录")
    
    return {
        "success": True,
        "message": f"API统计样本数据生成完成! 总共生成了 {total_calls} 条API调用记录",
        "total_calls": total_calls,
        "days_generated": days,
        "daily_stats": daily_stats
    }


async def generate_sample_data():
    """
    生成所有类型的样本数据
    
    包括:
    - API统计数据
    - (可以在未来添加更多类型的样本数据)
    
    Returns:
        生成结果统计
    """
    results = {}
    
    try:
        # 生成API统计数据
        logger.info("开始生成API统计数据...")
        results["api_stats"] = await generate_api_stats()
        
        # 未来可以在这里添加更多类型的样本数据生成
        
        return {
            "success": True,
            "message": "样本数据生成完成",
            "results": results
        }
    except Exception as e:
        logger.error(f"生成样本数据时出错: {e}")
        return {
            "success": False,
            "message": f"生成样本数据时出错: {e}",
            "results": results
        }


# 如果直接运行此模块，生成样本数据
if __name__ == "__main__":
    async def main():
        await init_db()
        try:
            await generate_sample_data()
        finally:
            await close_db()
    
    asyncio.run(main()) 