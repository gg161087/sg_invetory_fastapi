from fastapi import HTTPException, status
from app.config.dependency import db_dependency, user_dependency
from app.schemas.stock_location_schema import StockLocationCreate, StockLocationUpdate, StockLocationResponse
from app.services import stock_location_service
from app.auth.jwt_handler import check_user
import logging

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

def get_stock_locations(db: db_dependency, user: user_dependency, skip: int, limit: int):
    check_user(user)
    try:
        stock_location = stock_location_service.read_stock_location(db, skip=skip, limit=limit)
        return stock_location
    except Exception as e:
        logging.error(f'Error reading stock location: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')

def create_stock_location(stock_location: StockLocationCreate,  db: db_dependency, user: user_dependency):
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