from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Enum as SAEnum 
from src.core.database import Base
from src.enums.roles_enum import Roles

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, nullable=False)
    username = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    telefono = Column(String(50))
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(SAEnum(Roles), default=Roles.user)
    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())
