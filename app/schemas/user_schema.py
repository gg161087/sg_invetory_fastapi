from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.enums.roles_enum import Roles

class UserBase(BaseModel):
    email: str
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str
    telefono: Optional[str] = None
    is_active: bool
    role: Optional[Roles] = None

class UserCreate(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str
    role:str

class UserUpdate(UserBase):
    pass

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    telefono: Optional[str] = None
    is_active: bool
    role: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True