from fastapi import APIRouter, HTTPException, status
from typing import List
from src.core.dependency import db_dependency, user_dependency
from src.schemas.stock_location_schema import StockLocationCreate, StockLocationUpdate, StockLocationResponse
from src.services import stock_location_service
from src.core.security import check_user
import logging

router = APIRouter(
    prefix='/stock_location',
    tags=['Stock Location']    
)

@router.get('/{stock_location_id}', summary='GET Stock location by ID', response_model=StockLocationResponse)
def get_stock_location(stock_location_id: int, db: db_dependency, user: user_dependency):
    check_user(user)
    try:
        db_stock_location = stock_location_service.read_stock_location(db, stock_location_id)
        if db_stock_location is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Stock location not found')
        return db_stock_location
    except Exception as e:
        logging.error(f'Error reading stock location: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')

@router.get('/', summary='GET ALL Stock Location by Product', response_model=List[StockLocationResponse])
def get_stock_location(db: db_dependency, user: user_dependency, skip: int = 0, limit: int = 100):
    check_user(user)
    try:
        stock_location = stock_location_service.read_stock_location(db, skip=skip, limit=limit)
        return stock_location
    except Exception as e:
        logging.error(f'Error reading stock location: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')

@router.post('/', summary='CREATE a new Stock Location', status_code=status.HTTP_201_CREATED)
def create_stock_location_endpoint(stock_location: StockLocationCreate,  db: db_dependency, user: user_dependency):
    check_user(user)
    try:
        new_stock_location = stock_location_service.create_stock_location(db, stock_location.dict())
        if not new_stock_location:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error creating stock location')
        return new_stock_location
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logging.error(f'Error creating stock location: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')

@router.put('/{stock_location_id}', summary='UPDATE Stock Location by ID', response_model=StockLocationResponse)
def update_stock_movement(stock_location_id: int, stock_location_data: StockLocationUpdate, db: db_dependency, user: user_dependency):
    check_user(user)
    try:
        db_stock_location = stock_location_service.update_stock_location(db, stock_location_id, stock_location_data)
        if db_stock_location is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error updating stock location')
        return db_stock_location
    except Exception as e:
        logging.error(f'Error updating stock location: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')

@router.delete('/{stock_location_id}', summary='DELETE Stock Movement by ID', response_model=StockLocationResponse)
def delete_stock_location(stock_location_id: int, db: db_dependency, user: user_dependency):
    check_user(user)
    try:
        db_stock_location = stock_location_service.delete_stock_location(db, stock_location_id)
        if db_stock_location is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error deleting stock location')
        return db_stock_location
    except Exception as e:
        logging.error(f'Error deleting stock location: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')