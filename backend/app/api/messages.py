from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse

from app.core.deps import get_current_active_superuser, get_current_active_user
from app.models.message import Message
from app.models.user import User
from app.schemas.message import (
    MessageCreate,
    MessageOut,
    MessageUpdate,
)

router = APIRouter()


# 添加OPTIONS预检请求处理
@router.options("")
async def options_messages():
    return JSONResponse(
        status_code=200,
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
    )


@router.get("", response_model=List[MessageOut])
async def read_messages(
    skip: int = 0,
    limit: int = 20,
    is_read: Optional[bool] = None,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    获取消息列表（需要管理员权限）
    """
    query = Message.all()
    
    # 添加过滤条件
    if is_read is not None:
        query = query.filter(is_read=is_read)
    
    # 排序：按创建时间降序
    query = query.order_by("-created_at")
    
    # 分页
    messages = await query.offset(skip).limit(limit)
    
    return messages


@router.post("", response_model=MessageOut)
async def create_message(
    message_in: MessageCreate,
) -> Any:
    """
    创建新消息
    """
    message = Message(
        name=message_in.name,
        email=message_in.email,
        subject=message_in.subject,
        message=message_in.message,
    )
    await message.save()
    
    return message


@router.get("/{message_id}", response_model=MessageOut)
async def read_message(
    message_id: int,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    通过ID获取消息
    """
    message = await Message.filter(id=message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="消息不存在",
        )
    
    return message


@router.put("/{message_id}", response_model=MessageOut)
async def update_message(
    message_id: int,
    message_in: MessageUpdate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    更新消息状态
    """
    message = await Message.filter(id=message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="消息不存在",
        )
    
    # 更新已读状态
    message.is_read = message_in.is_read
    
    await message.save()
    
    return message


@router.delete("/{message_id}")
async def delete_message(
    message_id: int,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    删除消息
    """
    message = await Message.filter(id=message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="消息不存在",
        )
    
    # 删除消息
    await message.delete()
    
    return {"message": "消息已删除"} 