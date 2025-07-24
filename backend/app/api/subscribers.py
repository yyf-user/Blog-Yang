from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps import get_current_active_superuser
from app.models.subscriber import Subscriber
from app.models.user import User
from app.schemas.subscriber import SubscriberCreate, SubscriberOut, SubscriberUpdate

router = APIRouter()


@router.get("", response_model=List[SubscriberOut])
async def read_subscribers(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    获取所有订阅者列表
    """
    query = Subscriber.all()
    
    # 按状态筛选
    if status:
        query = query.filter(status=status)
    
    # 按创建时间降序排序
    query = query.order_by("-created_at")
    
    # 分页
    subscribers = await query.offset(skip).limit(limit)
    
    return subscribers


@router.post("", response_model=SubscriberOut)
async def create_subscriber(
    subscriber_in: SubscriberCreate,
) -> Any:
    """
    创建新订阅者
    """
    # 检查邮箱是否已存在
    existing_subscriber = await Subscriber.filter(email=subscriber_in.email).first()
    if existing_subscriber:
        # 如果已存在但状态是unsubscribed，则更新为active
        if existing_subscriber.status == "unsubscribed":
            existing_subscriber.status = "active"
            await existing_subscriber.save()
            return existing_subscriber
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已订阅",
        )
    
    # 创建订阅者
    subscriber = Subscriber(
        email=subscriber_in.email,
        status="active",
    )
    await subscriber.save()
    
    return subscriber


@router.get("/{subscriber_id}", response_model=SubscriberOut)
async def read_subscriber(
    subscriber_id: int,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    通过ID获取订阅者
    """
    subscriber = await Subscriber.filter(id=subscriber_id).first()
    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订阅者不存在",
        )
    
    return subscriber


@router.put("/{subscriber_id}", response_model=SubscriberOut)
async def update_subscriber(
    subscriber_id: int,
    subscriber_in: SubscriberUpdate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    更新订阅者状态
    """
    subscriber = await Subscriber.filter(id=subscriber_id).first()
    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订阅者不存在",
        )
    
    # 更新状态
    subscriber.status = subscriber_in.status
    
    await subscriber.save()
    
    return subscriber


@router.delete("/{subscriber_id}")
async def delete_subscriber(
    subscriber_id: int,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    删除订阅者
    """
    subscriber = await Subscriber.filter(id=subscriber_id).first()
    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订阅者不存在",
        )
    
    # 删除订阅者
    await subscriber.delete()
    
    return {"message": "订阅者已删除"}


@router.post("/unsubscribe/{email}")
async def unsubscribe(
    email: str,
) -> Any:
    """
    取消订阅
    """
    subscriber = await Subscriber.filter(email=email).first()
    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订阅者不存在",
        )
    
    # 更新状态为取消订阅
    subscriber.status = "unsubscribed"
    await subscriber.save()
    
    return {"message": "已成功取消订阅"} 