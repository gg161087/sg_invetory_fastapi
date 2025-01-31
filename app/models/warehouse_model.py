from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class Warehouse(BaseModel):
    __tablename__ = 'warehouse'
    name = Column(String(100), nullable=False, unique=True)
    address = Column(String(255), nullable=True)

    stock_locations = relationship('StockLocation', back_populates='warehouse')