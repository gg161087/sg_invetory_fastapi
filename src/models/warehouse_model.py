from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from src.core.database import Base

class Warehouse(Base):
    __tablename__ = 'warehouse'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    address = Column(String(255), nullable=True)
    createdAt = Column(DateTime, server_default=func.now(), nullable=False)
    updatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    stock_locations = relationship('StockLocation', back_populates='warehouse')
