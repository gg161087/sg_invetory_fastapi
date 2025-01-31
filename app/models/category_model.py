from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class Category(BaseModel):
    __tablename__ = 'category'    
    name = Column(String(60), nullable=False)
    description = Column(String(255), nullable=False)

    inventory_items = relationship('InventoryItem', back_populates='category')