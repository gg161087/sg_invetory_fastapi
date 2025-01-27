from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StockLocationBase(BaseModel):
    product_id: int
    name: str

class StockLocationCreate(StockLocationBase):
    entry_stock: Optional[int] = None

class StockLocationUpdate(BaseModel):
    name: Optional[str] = None
    entry_stock: Optional[int] = None

class StockLocationResponse(StockLocationBase):
    id: int
    createdAt: datetime
    updatedAt: datetime
    class Config:
        from_attributes = True
