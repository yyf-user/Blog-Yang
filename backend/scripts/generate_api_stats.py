#!/usr/bin/env python
"""
生成API统计数据脚本

此脚本用于生成真实的API调用统计数据，用于在管理后台展示。
"""

import asyncio
import random
from datetime import datetime, timedelta, date
from pathlib import Path
import sys

# 添加项目根目录到Python路径
project_root = Path(__file__).parents[1]
sys.path.append(str(project_root))

from app.models.api_stat import ApiStat, ApiStatDaily
from app.core.db import init_db


async def generate_api_stats():
    """生成API统计数据"""
    # 初始化数据库连接
    await init_db()
    
    print("开始生成API统计数据...")
    
    # 先清除现有的API统计数据
    await ApiStat.all().delete()
    await ApiStatDaily.all().delete()
    
    # 生成过去7天的数据
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
    
    # 生成每天的统计数据
    for day_offset in range(7):
        current_date = today - timedelta(days=day_offset)
        day_start = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = current_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # 为这一天生成的API调用次数
        # 越近的日期调用次数越多
        daily_calls = random.randint(50, 100) + (7 - day_offset) * 20
        
        # 今天的独立用户数
        unique_users_count = 0
        users_seen = set()
        
        # 今天的错误请求数
        error_count = 0
        
        # 今天的总响应时间
        total_response_time = 0
        
        print(f"为 {current_date.date()} 生成 {daily_calls} 条API调用记录...")
        
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
        
        # 计算今天的独立用户数
        unique_users_count = len(users_seen)
        
        # 计算今天的平均响应时间
        avg_response_time = (total_response_time / daily_calls) * 1000  # 转换为毫秒
        
        # 创建每日统计数据
        await ApiStatDaily.create(
            date=current_date.date(),
            total_calls=daily_calls,
            unique_users=unique_users_count,
            avg_response_time=avg_response_time,
            error_count=error_count
        )
    
    # 获取总调用次数
    total_stats = await ApiStat.all().count()
    print(f"生成完成! 总共生成了 {total_stats} 条API调用记录")
    
    # 打印每日统计数据
    daily_stats = await ApiStatDaily.all().order_by("date")
    print("\n每日统计数据:")
    for stat in daily_stats:
        print(f"日期: {stat.date}, 调用次数: {stat.total_calls}, 独立用户: {stat.unique_users}, "
              f"平均响应时间: {stat.avg_response_time:.2f}ms, 错误数: {stat.error_count}")


if __name__ == "__main__":
    asyncio.run(generate_api_stats()) 