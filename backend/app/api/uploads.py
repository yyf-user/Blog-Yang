import os
import uuid
from typing import Any, List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.deps import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.post("/avatar", response_model=dict)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    上传用户头像
    """
    # 检查文件类型
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只允许上传 JPEG、PNG、GIF 和 WebP 格式的图片",
        )
    
    # 检查文件大小
    file_size = 0
    contents = await file.read()
    file_size = len(contents)
    
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"文件大小不能超过 {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB",
        )
    
    # 确保头像上传目录存在
    upload_dir = os.path.join(settings.UPLOAD_DIR, "avatars")
    os.makedirs(upload_dir, exist_ok=True)
    
    # 生成唯一文件名
    file_ext = os.path.splitext(file.filename)[1]
    file_name = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(upload_dir, file_name)
    
    # 保存文件
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # 生成头像URL
    avatar_url = f"/api/uploads/avatars/{file_name}"
    
    # 更新用户头像URL
    current_user.avatar_url = avatar_url
    await current_user.save()
    
    return {
        "avatar_url": avatar_url,
        "filename": file_name,
        "content_type": file.content_type,
        "size": file_size,
    }


@router.get("/avatars/{file_name}")
async def get_avatar(file_name: str) -> Any:
    """
    获取上传的头像
    """
    file_path = os.path.join(settings.UPLOAD_DIR, "avatars", file_name)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="头像文件不存在",
        )
    
    return FileResponse(file_path)


@router.post("/images", response_model=dict)
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    上传图片文件
    """
    # 检查文件类型
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只允许上传 JPEG、PNG、GIF 和 WebP 格式的图片",
        )
    
    # 检查文件大小
    file_size = 0
    contents = await file.read()
    file_size = len(contents)
    
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"文件大小不能超过 {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB",
        )
    
    # 确保上传目录存在
    upload_dir = os.path.join(settings.UPLOAD_DIR, "images")
    os.makedirs(upload_dir, exist_ok=True)
    
    # 生成唯一文件名
    file_ext = os.path.splitext(file.filename)[1]
    file_name = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(upload_dir, file_name)
    
    # 保存文件
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # 返回文件URL
    file_url = f"/api/uploads/images/{file_name}"
    
    return {
        "url": file_url,
        "filename": file_name,
        "content_type": file.content_type,
        "size": file_size,
    }


@router.get("/images/{file_name}")
async def get_image(file_name: str) -> Any:
    """
    获取上传的图片
    """
    file_path = os.path.join(settings.UPLOAD_DIR, "images", file_name)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在",
        )
    
    return FileResponse(file_path)


@router.delete("/images/{file_name}")
async def delete_image(
    file_name: str,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    删除上传的图片
    """
    file_path = os.path.join(settings.UPLOAD_DIR, "images", file_name)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在",
        )
    
    # 删除文件
    os.remove(file_path)
    
    return {"message": "文件已删除"} 