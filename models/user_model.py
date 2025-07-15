from uuid import UUID
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

class UserBaseModel(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str] = None
    name: Optional[str] = None
    google_id: Optional[str] = None
    avatar_url: Optional[str] = None
    role: str = Field('customer')

class UserCreateModel(UserBaseModel):
    pass

class UserUpdateModel(UserBaseModel):
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    last_login: Optional[datetime] = None
    pass

class UserFullModel(UserBaseModel):
    id: UUID
    created_at: datetime
    last_login: Optional[datetime] = None