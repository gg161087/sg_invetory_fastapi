from sqlalchemy import Column, String, Boolean, Enum as SAEnum 
from app.enums.roles_enum import Roles
from app.models.base_model import BaseModel

class User(BaseModel):
    __tablename__ = 'user'
    email = Column(String(50), unique=True, nullable=False)
    username = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    telefono = Column(String(50))
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(SAEnum(Roles), default=Roles.user)