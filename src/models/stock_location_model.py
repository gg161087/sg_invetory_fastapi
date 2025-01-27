from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.core.database import Base

class StockLocation(Base):
    __tablename__ = 'stock_location'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=True)
    name = Column(String(60), nullable=False)
    entry_stock = Column(Integer, nullable=True)
    createdAt = Column(DateTime, server_default=func.now(), nullable=False)
    updatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    warehouse = relationship('Warehouse', back_populates='stock_locations')
    product = relationship('Product', back_populates='stock_locations')
    stock_movements = relationship('StockMovement', back_populates='stock_location')