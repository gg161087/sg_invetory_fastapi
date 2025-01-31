from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.stock_location_model import StockLocation
from app.models.inventory_item_model import InventoryItem
from app.schemas.stock_location_schema import StockLocationCreate, StockLocationUpdate
from app.models.stock_movement_model import StockMovement
import logging

def create_stock_location(db: Session, stock_location_data: dict):
    try:
        db_inventory_stock = db.query(InventoryItem).filter(InventoryItem.id == stock_location_data['InventoryItem_id']).first()
        if not db_inventory_stock:
            raise ValueError(f'Inventory Item with id {stock_location_data['InventoryItem_id']} does not exist.')
        if db_inventory_stock.current_stock is None or db_inventory_stock.current_stock < stock_location_data['entry_stock']:
            raise ValueError('Not enough stock available.')
        stock_location = StockLocation(**stock_location_data)
        db.add(stock_location)
        db.commit()
        db.refresh(stock_location)
        db_inventory_stock.current_stock -= stock_location.entry_stock
        db.commit()
        db.refresh(db_inventory_stock)
        stock_movement = StockMovement(
            product_id=db_inventory_stock.id,
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
        inventory_stock = db_stock_location.inventory_stock
        if inventory_stock:
            inventory_stock.current_stock = (inventory_stock.current_stock or 0) + stock
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