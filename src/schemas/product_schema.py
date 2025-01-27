from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from src.schemas.category_schema import CategoryResponse
from src.schemas.stock_location_schema import StockLocationResponse
class ProductBase(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    category_id: int
    initial_stock: Optional[int] = None
    current_stock: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    category: Optional[CategoryResponse]
    locations : Optional[List[StockLocationResponse]] = []
    createdAt: datetime
    updatedAt: datetime
    class Config:
        from_attributes = True
