from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WarehouseBase(BaseModel):
    name: str
    address: Optional[str]

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseUpdate(WarehouseBase):
    pass

class WarehouseResponse(WarehouseBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True