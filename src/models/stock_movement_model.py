from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.core.database import Base

class StockMovement(Base):
    __tablename__ = 'stock_movement'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    stock_location_id = Column(Integer, ForeignKey('stock_location.id'), nullable=True)
    movement_type = Column(String(20), nullable=False)
    quantity = Column(Integer, nullable=False)
    date = Column(DateTime, server_default=func.now(), nullable=False)
    reason = Column(String(255), nullable=True)

    product = relationship('Product', back_populates='stock_movements')
    stock_location = relationship('StockLocation', back_populates='stock_movements')
