from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class InventoryItem(BaseModel):
    __tablename__ = 'inventory_item'    
    sku = Column(String(50), nullable=False, unique=True)
    name = Column(String(60), nullable=False)
    description = Column(String(255), nullable=True)
    initial_stock = Column(Integer, nullable=True)
    current_stock = Column(Integer, nullable=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=True)

    category = relationship('Category', back_populates='inventory_items')
    stock_locations = relationship('StockLocation', back_populates='inventory_item')
    stock_movements = relationship('StockMovement', back_populates='inventory_item')