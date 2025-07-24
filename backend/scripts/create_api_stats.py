#!/usr/bin/env python
"""
API统计数据初始化脚本

此脚本用于在数据库中创建示例API统计数据，用于演示和开发目的。
它会创建各种API端点的调用记录，包括成功和错误请求。
"""

import asyncio
import random
from datetime import datetime, timedelta, date

from tortoise import Tortoise

from app.core.config import settings
from app.models.api_stat import ApiStat, ApiStatDaily


async def init():
    # 连接到数据库
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models"]},
    )
    
    # 清除现有API统计数据
    print("清除现有API统计数据...")
    await ApiStat.all().delete()
    await ApiStatDaily.all().delete()
    
    print("开始创建新的API统计数据...")
    
    # 创建示例API端点数据 - 定义每个端点需要创建的记录数和错误率
    example_endpoints = [
        {"path": "/api/articles", "method": "GET", "success_count": 120, "error_count": 12, "avg_response_time": 98},
        {"path": "/api/articles/{id}", "method": "GET", "success_count": 80, "error_count": 8, "avg_response_time": 112},
        {"path": "/api/articles/by-slug/{slug}", "method": "GET", "success_count": 60, "error_count": 6, "avg_response_time": 125},
        {"path": "/api/articles", "method": "POST", "success_count": 25, "error_count": 4, "avg_response_time": 320},
        {"path": "/api/articles/{id}", "method": "PUT", "success_count": 15, "error_count": 2, "avg_response_time": 268},
        
        {"path": "/api/auth/login", "method": "POST", "success_count": 70, "error_count": 12, "avg_response_time": 245},
        {"path": "/api/auth/register", "method": "POST", "success_count": 20, "error_count": 5, "avg_response_time": 380},
        
        {"path": "/api/users/me", "method": "GET", "success_count": 50, "error_count": 5, "avg_response_time": 87},
        {"path": "/api/users", "method": "GET", "success_count": 25, "error_count": 2, "avg_response_time": 124},
        
        {"path": "/api/projects", "method": "GET", "success_count": 70, "error_count": 4, "avg_response_time": 105},
        {"path": "/api/projects/{id}", "method": "GET", "success_count": 40, "error_count": 3, "avg_response_time": 118},
        
        {"path": "/api/tags", "method": "GET", "success_count": 35, "error_count": 1, "avg_response_time": 65},
        
        {"path": "/api/messages", "method": "POST", "success_count": 30, "error_count": 5, "avg_response_time": 280},
        
        {"path": "/api/stats/api", "method": "GET", "success_count": 25, "error_count": 3, "avg_response_time": 248},
        
        {"path": "/api/uploads/image", "method": "POST", "success_count": 15, "error_count": 2, "avg_response_time": 342},
        
        {"path": "/api/subscribers", "method": "POST", "success_count": 20, "error_count": 3, "avg_response_time": 164},
    ]
    
    # 模拟一些用户ID和匿名访问
    user_ids = [1, 2, 3, 4, 5, None]
    
    total_records = 0
    
    # 为每个端点创建API调用记录
    print("创建API调用记录...")
    
    # 创建过去7天的数据
    for days_ago in range(7):
        day_date = datetime.now() - timedelta(days=days_ago)
        
        # 工作日创建更多记录
        day_multiplier = 0.7 if day_date.weekday() >= 5 else 1.0  # 周末记录少一些
        
        for endpoint in example_endpoints:
            # 根据天数调整创建的记录数量
            success_count = int(endpoint["success_count"] * day_multiplier * (0.7 + 0.3 * random.random()))
            error_count = int(endpoint["error_count"] * day_multiplier * (0.7 + 0.3 * random.random()))
            
            # 创建成功请求
            for _ in range(success_count):
                time_of_day = random.randint(8, 23)  # 8am - 11pm
                timestamp = day_date.replace(
                    hour=time_of_day, 
                    minute=random.randint(0, 59),
                    second=random.randint(0, 59)
                )
                
                # 添加一些随机性到响应时间
                response_time = endpoint["avg_response_time"] * (0.8 + 0.4 * random.random()) / 1000.0  # 转换为秒
                
                await ApiStat.create(
                    endpoint=endpoint["path"],
                    method=endpoint["method"],
                    status_code=200,
                    response_time=response_time,
                    timestamp=timestamp,
                    user_id=random.choice(user_ids)
                )
                total_records += 1
            
            # 创建错误请求
            for _ in range(error_count):
                time_of_day = random.randint(8, 23)  # 8am - 11pm
                timestamp = day_date.replace(
                    hour=time_of_day, 
                    minute=random.randint(0, 59),
                    second=random.randint(0, 59)
                )
                
                error_code = random.choice([400, 401, 403, 404, 500])
                
                # 错误请求通常响应时间更长
                response_time = endpoint["avg_response_time"] * (1.2 + 0.6 * random.random()) / 1000.0
                
                await ApiStat.create(
                    endpoint=endpoint["path"],
                    method=endpoint["method"],
                    status_code=error_code,
                    response_time=response_time,
                    timestamp=timestamp,
                    user_id=random.choice(user_ids)
                )
                total_records += 1
    
    print(f"已创建 {total_records} 条API调用记录")
    
    # 创建每日统计数据
    print("创建每日统计数据...")
    today = date.today()
    daily_stats = []
    
    for i in range(7):
        day = today - timedelta(days=i)
        
        # 生成合理的调用次数（工作日比周末多）
        day_of_week = day.weekday()  # 0=周一, 6=周日
        if day_of_week >= 5:  # 周末
            calls = random.randint(200, 350)
            users = random.randint(10, 20)
        else:  # 工作日
            calls = random.randint(350, 650)
            users = random.randint(15, 30)
        
        errors = int(calls * random.uniform(0.02, 0.08))  # 2-8%错误率
        
        daily_stat = await ApiStatDaily.create(
            date=day,
            total_calls=calls,
            unique_users=users,
            avg_response_time=random.randint(120, 220),
            error_count=errors
        )
        daily_stats.append(daily_stat)
    
    print(f"已创建 {len(daily_stats)} 天的API每日统计数据")
    
    # 更新其他统计数据
    print("更新所有统计数据...")
    from app.core.update_stats import update_all_stats
    await update_all_stats()
    print("所有统计数据已更新")
    
    # 关闭数据库连接
    await Tortoise.close_connections()
    
    print("API统计数据初始化完成!")


if __name__ == "__main__":
    asyncio.run(init()) 