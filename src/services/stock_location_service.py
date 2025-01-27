from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.models.stock_location_model import StockLocation
from src.models.product_model import Product
from src.schemas.stock_location_schema import StockLocationCreate, StockLocationUpdate
from src.models.stock_movement_model import StockMovement
import logging

def create_stock_location(db: Session, stock_location_data: dict):
    try:
        product = db.query(Product).filter(Product.id == stock_location_data['product_id']).first()
        if not product:
            raise ValueError(f'Product with id {stock_location_data["product_id"]} does not exist.')
        if product.current_stock is None or product.current_stock < stock_location_data['entry_stock']:
            raise ValueError('Not enough stock available.')
        stock_location = StockLocation(**stock_location_data)
        db.add(stock_location)
        db.commit()
        db.refresh(stock_location)
        product.current_stock -= stock_location.entry_stock
        db.commit()
        db.refresh(product)
        stock_movement = StockMovement(
            product_id=product.id,
            stock_location_id=stock_location.id,
            movement_type='entry',
            quantity=stock_location.entry_stock,
            reason='Stock assigned to location'
        )
        db.add(stock_movement)
        db.commit()
        return stock_location
    except SQLAlchemyError as e:
        logging.error(f'Error creating stock location: {e}')
        db.rollback()
        return None

def read_stock_location(db: Session, stock_location_id: int):
    try:
        return db.query(StockLocation).filter(StockLocation.id == stock_location_id).first()
    except SQLAlchemyError as e:
        logging.error(f'Error reading stock location: {e}')
        raise RuntimeError(f'Could not read stock location: {e}')

def read_stock_locations(db: Session, product_id: int = None, skip: int = 0, limit: int = 100):
    try:
        query = db.query(StockLocation)
        if product_id:
            query = query.filter(StockLocation.product_id == product_id)
        return query.offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logging.error(f'Error reading stock locations: {e}')
        return None

def update_stock_location(db: Session, stock_location_id: int, stock_location: StockLocationUpdate):
    try:
        db_stock_location = db.query(StockLocation).filter(StockLocation.id == stock_location_id).first()
        if not db_stock_location:
            raise ValueError(f'Stock location with id {stock_location_id} does not exist.')
        for key, value in stock_location.dict(exclude_unset=True).items():
            setattr(db_stock_location, key, value)
        db.commit()
        db.refresh(db_stock_location)
        return db_stock_location
    except SQLAlchemyError as e:
        logging.error(f'Error updating stock location: {e}')
        db.rollback()
        return None

def assign_stock_to_location(db: Session, stock_location_id: int, stock: int):
    try:
        db_stock_location = db.query(StockLocation).filter(StockLocation.id == stock_location_id).first()
        if not db_stock_location:
            raise ValueError(f'Stock location with id {stock_location_id} does not exist.')
        db_stock_location.entry_stock = (db_stock_location.entry_stock or 0) + stock
        product = db_stock_location.product
        if product:
            product.current_stock = (product.current_stock or 0) + stock
        db.commit()
        db.refresh(db_stock_location)
        return db_stock_location
    except SQLAlchemyError as e:
        logging.error(f'Error assigning stock to location: {e}')
        db.rollback()
        return None

def delete_stock_location(db: Session, stock_location_id: int):
    try:
        db_stock_location = db.query(StockLocation).filter(StockLocation.id == stock_location_id).first()
        if not db_stock_location:
            raise ValueError(f'Stock location with id {stock_location_id} does not exist.')
        db.delete(db_stock_location)
        db.commit()
        return db_stock_location
    except SQLAlchemyError as e:
        logging.error(f'Error deleting stock location: {e}')
        db.rollback()
        return None