from datetime import timedelta
from typing import Any
import logging

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserOut
from app.utils.slug import generate_username_slug

router = APIRouter()
logger = logging.getLogger("app.api.auth")


# 添加OPTIONS预检请求处理
@router.options("/login")
async def options_login():
    return JSONResponse(
        status_code=200,
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
    )


@router.options("/register")
async def options_register():
    return JSONResponse(
        status_code=200,
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
    )


@router.post("/login", response_model=Token)
async def login_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 兼容的令牌登录，获取访问令牌
    """
    logger.info(f"尝试登录用户: {form_data.username}")
    client_host = request.client.host if request.client else "unknown"
    logger.info(f"请求来源IP: {client_host}")
    
    user = await User.filter(username=form_data.username).first()
    if not user:
        logger.warning(f"登录失败: 用户名不存在 - {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码不正确",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.verify_password(form_data.password):
        logger.warning(f"登录失败: 密码错误 - {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码不正确",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 创建访问令牌
    access_token = create_access_token(
        user.id, expires_delta=access_token_expires
    )
    
    logger.info(f"用户登录成功: {user.username}")
    
    # 返回令牌
    # 注意：这里只返回令牌信息，不返回用户信息，前端会通过/users/me获取用户信息
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/register", response_model=UserOut)
async def register_user(
    request: Request,
    user_in: UserCreate
) -> Any:
    """
    注册新用户
    """
    logger.info(f"尝试注册新用户: {user_in.username}, 邮箱: {user_in.email}")
    client_host = request.client.host if request.client else "unknown"
    logger.info(f"请求来源IP: {client_host}")
    
    # 检查用户名是否已存在
    existing_user = await User.filter(username=user_in.username).first()
    if existing_user:
        logger.warning(f"注册失败: 用户名已存在 - {user_in.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该用户名已被注册",
        )
    
    # 检查邮箱是否已存在
    existing_email = await User.filter(email=user_in.email).first()
    if existing_email:
        logger.warning(f"注册失败: 邮箱已存在 - {user_in.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册",
        )
    
    # 创建新用户
    user_obj = User(
        username=user_in.username,
        email=user_in.email,
        full_name=user_in.full_name,
        bio=user_in.bio,
        avatar_url=user_in.avatar_url,
        github_url=user_in.github_url,
        linkedin_url=user_in.linkedin_url,
        twitter_url=user_in.twitter_url,
        website_url=user_in.website_url,
    )
    # 设置密码
    await user_obj.set_password(user_in.password)
    # 保存用户
    await user_obj.save()
    
    logger.info(f"用户注册成功: {user_obj.username}")
    
    return UserOut.from_orm(user_obj) 