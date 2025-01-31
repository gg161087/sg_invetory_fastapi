from fastapi import APIRouter, status
from app.schemas.stock_movement_schema import StockMovementCreate
from app.config.dependency import db_dependency, user_dependency
from app.controllers import stock_movement_controller

router = APIRouter(prefix='/stock_movement', tags=['Stock Movement'])

@router.post('/', summary='CREATE new Stock Movement', status_code=status.HTTP_201_CREATED)
def create_stock_movement(stock_movement: StockMovementCreate, db: db_dependency, user: user_dependency):
    return stock_movement_controller.create_stock_movement(stock_movement, db, user)