from typing import Optional

from pydantic import BaseModel, EmailStr


# 共享属性
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None
    website_url: Optional[str] = None


# 用于创建用户时
class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: str


# 用于更新用户时
class UserUpdate(UserBase):
    password: Optional[str] = None


# 用于更新用户密码
class UserUpdatePassword(BaseModel):
    current_password: str
    new_password: str


# 用于更新用户角色时
class UserUpdateRole(BaseModel):
    role: str


# 用于返回给API的用户信息
class UserOut(UserBase):
    id: int
    username: str
    role: str
    
    class Config:
        from_attributes = True


# 用于返回包含更多详细信息的用户信息
class UserDetail(UserOut):
    pass 