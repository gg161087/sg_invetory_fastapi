from pydantic import BaseModel
from typing import Optional

class StockMovementCreate(BaseModel):
    product_id: int
    stock_location_id: Optional[int] = None
    movement_type: str
    quantity: int
    reason: Optional[str] = None

    class Config:
        orm_mode = True
