from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.category_schema import CategoryResponse
from app.schemas.stock_location_schema import StockLocationResponse

class InventoryItemBase(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    category_id: int
    initial_stock: Optional[int] = None
    current_stock: Optional[int] = None

class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItemUpdate(InventoryItemBase):
    pass

class InventoryItemResponse(InventoryItemBase):
    id: int
    category: Optional[CategoryResponse]
    locations : Optional[List[StockLocationResponse]] = []
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
