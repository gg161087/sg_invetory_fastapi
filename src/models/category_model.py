from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from src.core.database import Base

class Category(Base):
    __tablename__ = 'category'    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60), nullable=False)
    description = Column(String(255), nullable=False)
    createdAt = Column(DateTime, server_default=func.now(), nullable=False)
    updatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    products = relationship('Product', back_populates='category')