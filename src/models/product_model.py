from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from src.core.database import Base

class Product(Base):
    __tablename__ = 'product'    
    id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String(50), nullable=False, unique=True)
    name = Column(String(60), nullable=False)
    description = Column(String(255), nullable=True)
    initial_stock = Column(Integer, nullable=True)
    current_stock = Column(Integer, nullable=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=True)
    createdAt = Column(DateTime, server_default=func.now(), nullable=False)
    updatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    category = relationship('Category', back_populates='products')
    stock_locations = relationship('StockLocation', back_populates='product')
    stock_movements = relationship('StockMovement', back_populates='product')