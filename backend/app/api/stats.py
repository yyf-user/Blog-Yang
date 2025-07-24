from typing import Any, Dict, List
from datetime import timedelta, date, datetime, time
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.core.deps import get_current_active_superuser
from app.models.stat import Stat
from app.models.api_stat import ApiStat, ApiStatDaily
from app.models.user import User
from app.schemas.stat import StatCreate, StatOut, StatUpdate


router = APIRouter()


async def update_all_stats() -> Dict[str, Any]:
    """
    更新所有统计数据
    
    此函数用于更新各种统计数据，如文章数、用户数等。
    同时更新API统计的独立用户数。
    
    Returns:
        Dict[str, Any]: 更新结果
    """
    try:
        # 更新文章数
        from app.models.article import Article
        article_count = await Article.all().count()
        article_stat = await Stat.filter(key="article_count").first()
        if article_stat:
            article_stat.value = article_count
            await article_stat.save()
        else:
            await Stat.create(
                key="article_count",
                value=article_count,
                display_text="文章数量"
            )
        
        # 更新用户数
        user_count = await User.all().count()
        user_stat = await Stat.filter(key="user_count").first()
        if user_stat:
            user_stat.value = user_count
            await user_stat.save()
        else:
            await Stat.create(
                key="user_count",
                value=user_count,
                display_text="用户数量"
            )
        
        # 更新项目数
        from app.models.project import Project
        project_count = await Project.all().count()
        project_stat = await Stat.filter(key="project_count").first()
        if project_stat:
            project_stat.value = project_count
            await project_stat.save()
        else:
            await Stat.create(
                key="project_count",
                value=project_count,
                display_text="项目数量"
            )
        
        # 更新消息数
        from app.models.message import Message
        message_count = await Message.all().count()
        message_stat = await Stat.filter(key="message_count").first()
        if message_stat:
            message_stat.value = message_count
            await message_stat.save()
        else:
            await Stat.create(
                key="message_count",
                value=message_count,
                display_text="消息数量"
            )
        
        # 更新API统计的独立用户数
        today = date.today()
        daily_stat = await ApiStatDaily.filter(date=today).first()
        if daily_stat:
            # 获取今天的独立用户数
            today_start = datetime.combine(today, time.min)
            today_end = datetime.combine(today, time.max)
            unique_users = len(set(
                stat.user_id for stat in await ApiStat.filter(
                    timestamp__gte=today_start,
                    timestamp__lte=today_end
                ).filter(user_id__isnull=False)
            ))
            daily_stat.unique_users = unique_users
            await daily_stat.save()
        
        return {
            "success": True,
            "message": "统计数据已更新",
            "stats": {
                "article_count": article_count,
                "user_count": user_count,
                "project_count": project_count,
                "message_count": message_count
            }
        }
    except Exception as e:
        print(f"更新统计数据出错: {e}")
        return {
            "success": False,
            "message": f"更新统计数据出错: {e}"
        }


@router.get("", response_model=List[StatOut])
async def read_stats() -> Any:
    """
    获取所有统计数据
    """
    stats = await Stat.all()
    return stats


@router.get("/dashboard", response_model=Dict[str, int])
async def read_dashboard_stats() -> Any:
    """
    获取仪表盘统计数据
    """
    stats = await Stat.all()
    result = {}
    for stat in stats:
        result[stat.key] = stat.value
    return result


@router.get("/api")
async def read_api_stats() -> Any:
    """
    获取API调用统计信息
    """
    try:
        # 获取API统计数据
        api_stats = await ApiStat.all()
        
        # 如果没有数据，返回空结果而不是模拟数据
        if not api_stats:
            return JSONResponse(content={
                "total_calls": 0,
                "unique_users": 0,
                "avg_response_time": 0,
                "error_rate": 0,
                "endpoints": []
            })
        
        # 计算每个端点的统计信息
        endpoint_stats = {}
        
        for stat in api_stats:
            key = f"{stat.method}|{stat.endpoint}"
            
            if key not in endpoint_stats:
                endpoint_stats[key] = {
                    "path": stat.endpoint,
                    "method": stat.method,
                    "calls": 0,
                    "avg_response_time": 0,
                    "error_count": 0,
                    "total_response_time": 0,
                    "last_call": stat.timestamp
                }
            
            endpoint_stats[key]["calls"] += 1
            endpoint_stats[key]["total_response_time"] += stat.response_time
            
            if stat.is_error:
                endpoint_stats[key]["error_count"] += 1
            
            if stat.timestamp > endpoint_stats[key]["last_call"]:
                endpoint_stats[key]["last_call"] = stat.timestamp
        
        # 计算平均响应时间和错误率
        for key in endpoint_stats:
            stats = endpoint_stats[key]
            stats["avg_response_time"] = round((stats["total_response_time"] / stats["calls"]) * 1000, 1)  # 转换为毫秒
            stats["error_rate"] = round((stats["error_count"] / stats["calls"]) * 100, 1)
            del stats["total_response_time"]  # 删除中间计算值
        
        # 计算总调用次数
        total_calls = len(api_stats)
        
        # 计算平均响应时间
        avg_response_time = round(sum(stat.response_time for stat in api_stats) / total_calls * 1000, 1) if total_calls > 0 else 0
        
        # 计算错误率
        error_count = sum(1 for stat in api_stats if stat.is_error)
        error_rate = round(error_count / total_calls * 100, 1) if total_calls > 0 else 0
        
        # 获取独立用户数
        unique_users = len(set(stat.user_id for stat in api_stats if stat.user_id is not None))
        
        # 构建响应
        result = {
            "total_calls": total_calls,
            "unique_users": unique_users,
            "avg_response_time": avg_response_time,
            "error_rate": error_rate,
            "endpoints": list(endpoint_stats.values())
        }
        
        return JSONResponse(content=result)
    except Exception as e:
        print(f"获取API统计信息出错: {e}")
        # 返回空结果，不使用模拟数据
        return JSONResponse(content={
            "total_calls": 0,
            "unique_users": 0,
            "avg_response_time": 0,
            "error_rate": 0,
            "endpoints": []
        })


@router.get("/api/trends")
async def read_api_trends() -> Any:
    """
    获取API调用趋势数据
    """
    try:
        # 获取最近7天的API调用数据
        today = date.today()
        start_date = today - timedelta(days=6)
        
        # 按日期分组计算每天的调用次数
        trend_data = {}
        
        for i in range(7):
            day = (today - timedelta(days=i)).isoformat()
            trend_data[day] = 0
        
        # 查询每天的API调用次数
        api_stats = await ApiStat.all()
        
        # 不再使用模拟数据，直接使用真实数据
        for stat in api_stats:
            day = stat.timestamp.date().isoformat()
            if day in trend_data:
                trend_data[day] += 1
        
        # 构建响应
        trends = []
        for day, count in trend_data.items():
            trends.append({
                "date": day,
                "count": count  # 使用真实的调用次数
            })
        
        # 按日期排序
        trends.sort(key=lambda x: x["date"])
        
        return JSONResponse(content=trends)
    except Exception as e:
        print(f"获取API趋势数据出错: {e}")
        # 返回空数据，不使用模拟数据
        empty_data = []
        for i in range(7):
            day = (today - timedelta(days=i)).isoformat()
            empty_data.append({
                "date": day,
                "count": 0
            })
        # 按日期排序
        empty_data.sort(key=lambda x: x["date"])
        return JSONResponse(content=empty_data)


@router.get("/api/{endpoint}")
async def read_api_detail(endpoint: str) -> Any:
    """
    获取特定API的调用详情
    """
    try:
        # 构建路径
        path = f"/api/{endpoint}"
        
        # 查找API统计数据
        api_stats = await ApiStat.filter(endpoint=path)
        
        # 如果没有找到，返回空数据
        if not api_stats:
            return JSONResponse(content={
                "path": path,
                "methods": [],
                "total_calls": 0,
                "avg_response_time": 0,
                "error_rate": 0,
                "status_codes": {}
            })
        
        # 计算统计信息
        total_calls = len(api_stats)
        methods = list(set(stat.method for stat in api_stats))
        avg_response_time = round(sum(stat.response_time for stat in api_stats) / total_calls * 1000, 1) if total_calls > 0 else 0
        
        # 计算错误率
        error_count = sum(1 for stat in api_stats if stat.is_error)
        error_rate = round(error_count / total_calls * 100, 1) if total_calls > 0 else 0
        
        # 统计状态码
        status_codes = {}
        for stat in api_stats:
            code = str(stat.status_code)
            status_codes[code] = status_codes.get(code, 0) + 1
        
        # 构建响应
        result = {
            "path": path,
            "methods": methods,
            "total_calls": total_calls,
            "avg_response_time": avg_response_time,
            "error_rate": error_rate,
            "status_codes": status_codes
        }
        
        return JSONResponse(content=result)
    except Exception as e:
        print(f"获取API详情出错: {e}")
        # 返回空结果
        return JSONResponse(content={
            "path": f"/api/{endpoint}",
            "methods": [],
            "total_calls": 0,
            "avg_response_time": 0,
            "error_rate": 0,
            "status_codes": {}
        })


@router.post("", response_model=StatOut)
async def create_stat(
    stat_in: StatCreate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    创建新统计数据
    """
    # 检查key是否已存在
    existing_stat = await Stat.filter(key=stat_in.key).first()
    if existing_stat:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该统计数据key已存在",
        )
    
    # 创建统计数据
    stat = Stat(
        key=stat_in.key,
        value=stat_in.value,
        display_text=stat_in.display_text,
    )
    await stat.save()
    
    return stat


@router.get("/{stat_id}", response_model=StatOut)
async def read_stat(
    stat_id: int,
) -> Any:
    """
    通过ID获取统计数据
    """
    stat = await Stat.filter(id=stat_id).first()
    if not stat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="统计数据不存在",
        )
    
    return stat


@router.put("/{stat_id}", response_model=StatOut)
async def update_stat(
    stat_id: int,
    stat_in: StatUpdate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    更新统计数据
    """
    stat = await Stat.filter(id=stat_id).first()
    if not stat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="统计数据不存在",
        )
    
    # 如果更改key，检查新key是否已存在
    if stat_in.key is not None and stat_in.key != stat.key:
        existing_stat = await Stat.filter(key=stat_in.key).first()
        if existing_stat:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该统计数据key已存在",
            )
        stat.key = stat_in.key
    
    # 更新其他字段
    if stat_in.value is not None:
        stat.value = stat_in.value
    
    if stat_in.display_text is not None:
        stat.display_text = stat_in.display_text
    
    await stat.save()
    
    return stat


@router.delete("/{stat_id}")
async def delete_stat(
    stat_id: int,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    删除统计数据
    """
    stat = await Stat.filter(id=stat_id).first()
    if not stat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="统计数据不存在",
        )
    
    # 删除统计数据
    await stat.delete()
    
    return {"message": "统计数据已删除"} 