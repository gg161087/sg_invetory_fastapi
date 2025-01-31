from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class StockLocation(BaseModel):
    __tablename__ = 'stock_location'
    inventory_item_id = Column(Integer, ForeignKey('inventory_item.id'), nullable=True)
    name = Column(String(60), nullable=False)
    entry_stock = Column(Integer, nullable=True)
    warehouse_id = Column(Integer, ForeignKey('warehouse.id'))

    inventory_item = relationship('InventoryItem', back_populates='stock_locations')
    stock_movements = relationship('StockMovement', back_populates='stock_location')
    warehouse = relationship('Warehouse', back_populates='stock_locations')