from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError

from app.core.config import settings
from app.models.user import User
from app.schemas.token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    auto_error=False  # 设置为False使令牌可选
)


async def get_current_user(
    token: str = Depends(reusable_oauth2)
) -> User:
    """
    获取当前用户
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无法验证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await User.filter(id=token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    获取当前活跃用户
    """
    return current_user


async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    获取当前活跃超级用户
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足",
        )
    return current_user


async def get_optional_user(
    token: Optional[str] = Depends(reusable_oauth2)
) -> Optional[User]:
    """
    获取当前用户（可选的）
    如果提供了有效令牌，返回用户对象；否则返回None
    """
    if not token:
        return None
    
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        token_data = TokenPayload(**payload)
        user = await User.filter(id=token_data.sub).first()
        return user
    except (JWTError, ValidationError):
        return None 