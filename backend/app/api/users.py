from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps import get_current_active_superuser, get_current_active_user
from app.models.user import User
from app.schemas.user import UserDetail, UserOut, UserUpdate, UserUpdateRole, UserUpdatePassword

router = APIRouter()


@router.get("/me", response_model=UserDetail)
async def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    获取当前用户
    """
    return current_user


@router.put("/me", response_model=UserDetail)
async def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    更新当前用户
    """
    if user_in.email is not None:
        # 检查邮箱是否已存在
        existing_user = await User.filter(email=user_in.email).exclude(id=current_user.id).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该邮箱已被注册",
            )
        current_user.email = user_in.email
    
    # 更新其他字段
    if user_in.full_name is not None:
        current_user.full_name = user_in.full_name
    if user_in.bio is not None:
        current_user.bio = user_in.bio
    if user_in.avatar_url is not None:
        current_user.avatar_url = user_in.avatar_url
    if user_in.github_url is not None:
        current_user.github_url = user_in.github_url
    if user_in.linkedin_url is not None:
        current_user.linkedin_url = user_in.linkedin_url
    if user_in.twitter_url is not None:
        current_user.twitter_url = user_in.twitter_url
    if user_in.website_url is not None:
        current_user.website_url = user_in.website_url
    if user_in.password:
        await current_user.set_password(user_in.password)
    
    await current_user.save()
    return current_user


@router.put("/me/password", response_model=UserDetail)
async def update_user_password(
    password_in: UserUpdatePassword,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    更新当前用户密码
    """
    # 验证当前密码
    if not current_user.verify_password(password_in.current_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="当前密码不正确",
        )
    
    # 设置新密码
    await current_user.set_password(password_in.new_password)
    await current_user.save()
    
    return current_user


@router.get("", response_model=List[UserOut])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    获取所有用户列表
    """
    users = await User.all().offset(skip).limit(limit)
    return users


@router.get("/{user_id}", response_model=UserDetail)
async def read_user(
    user_id: int,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    通过ID获取用户
    """
    user = await User.filter(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    return user


@router.put("/{user_id}/role", response_model=UserOut)
async def update_user_role(
    user_id: int,
    user_in: UserUpdateRole,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    更新用户角色
    """
    user = await User.filter(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    
    # 检查角色是否有效
    if user_in.role not in ["admin", "user"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的角色",
        )
    
    user.role = user_in.role
    await user.save()
    return user 