from fastapi import APIRouter, status
from typing import List
from app.config.dependency import db_dependency, user_dependency
from app.schemas.stock_location_schema import StockLocationCreate, StockLocationUpdate, StockLocationResponse
from app.controllers import stock_location_controller

router = APIRouter(prefix='/stock_location', tags=['Stock Location'])

@router.get('/{stock_location_id}', summary='GET Stock location by ID', response_model=StockLocationResponse)
def get_stock_location(stock_location_id: int, db: db_dependency, user: user_dependency):
    return stock_location_controller.get_stock_location(stock_location_id, db, user)

@router.get('/', summary='GET ALL Stock Location by Product', response_model=List[StockLocationResponse])
def get_stock_locations(db: db_dependency, user: user_dependency, skip: int = 0, limit: int = 100):
    return stock_location_controller.get_stock_locations(db, user, skip, limit)

@router.post('/', summary='CREATE a new Stock Location', status_code=status.HTTP_201_CREATED)
def create_stock_location(stock_location: StockLocationCreate,  db: db_dependency, user: user_dependency):
    return stock_location_controller.create_stock_location(stock_location, db, user)

@router.put('/{stock_location_id}', summary='UPDATE Stock Location by ID', response_model=StockLocationResponse)
def update_stock_movement(stock_location_id: int, stock_location_data: StockLocationUpdate, db: db_dependency, user: user_dependency):
    return stock_location_controller.update_stock_movement(stock_location_id, stock_location_data, db, user)

@router.delete('/{stock_location_id}', summary='DELETE Stock Movement by ID', response_model=StockLocationResponse)
def delete_stock_location(stock_location_id: int, db: db_dependency, user: user_dependency):
    return stock_location_controller.delete_stock_location(stock_location_id, db, user)