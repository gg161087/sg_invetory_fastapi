from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class StockMovement(BaseModel):
    __tablename__ = 'stock_movement'
    product_id = Column(Integer, ForeignKey('inventory_item.id'), nullable=False)
    stock_location_id = Column(Integer, ForeignKey('stock_location.id'), nullable=True)
    movement_type = Column(String(20), nullable=False)
    quantity = Column(Integer, nullable=False)
    date = Column(DateTime, server_default=func.now(), nullable=False)
    reason = Column(String(255), nullable=True)

    inventory_item = relationship('InventoryItem', back_populates='stock_movements')
    stock_location = relationship('StockLocation', back_populates='stock_movements')