from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.inventory_item_model import InventoryItem
from app.schemas.inventory_item_schema import InventoryItemCreate, InventoryItemUpdate
import logging

def create_inventory_item(db: Session, inventory_item_data: InventoryItemCreate):
    try:
        inventory_item_dict = inventory_item_data.dict()
        inventory_item_dict['initial_stock'] = inventory_item_dict.get('initial_stock', None)
        inventory_item_dict['current_stock'] = inventory_item_dict.get('current_stock', None)
        db_inventory_item = InventoryItem(**inventory_item_dict)
        db.add(db_inventory_item)
        db.commit()
        db.refresh(db_inventory_item)
        return db_inventory_item
    except SQLAlchemyError as e:
        logging.error(f'Error creating inventory_item: {e}')
        db.rollback()
        raise None

def read_inventory_item(db: Session, inventory_item_id: int):
    try:
        return db.query(InventoryItem).filter(InventoryItem.id == inventory_item_id).first()
    except SQLAlchemyError as e:
        logging.error(f'Error reading inventory item: {e}')
        return None
    
def read_inventory_item_by_sku(db: Session, sku: str):
    try:
        return db.query(InventoryItem).filter(InventoryItem.sku == sku).first()
    except SQLAlchemyError as e:
        logging.error(f'Error reading inventory item: {e}')
        return None

def read_inventory_items(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(InventoryItem).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logging.error(f'Error reading inventory items: {e}')
        return None

def update_inventory_item(db: Session, inventory_item_id: int, inventory_item_data: InventoryItemUpdate):
    try:
        db_inventory_item = db.query(InventoryItem).filter(InventoryItem.id == inventory_item_id).first()
        if not db_inventory_item:
            raise ValueError(f'Inventory Item with id {inventory_item_id} does not exist.')

        for key, value in inventory_item_data.dict(exclude_unset=True).items():
            setattr(db_inventory_item, key, value)
        db.commit()
        db.refresh(db_inventory_item)
        return db_inventory_item
    except SQLAlchemyError as e:
        logging.error(f'Error updating inventory item: {e}')
        db.rollback()
        return None
    
def update_inventory_item_stock(db: Session, inventory_item_id: int, quantity: int):
    try:
        db_inventory_item = db.query(InventoryItem).filter(InventoryItem.id == inventory_item_id).first()
        if db_inventory_item:
            if db_inventory_item.current_stock is None:
                db_inventory_item.current_stock = 0
            if db_inventory_item.current_stock + quantity < 0:
                raise ValueError('Insufficient stock')
            db_inventory_item.current_stock += quantity
            db.commit()
            db.refresh(db_inventory_item)
            return db_inventory_item
        return None
    except SQLAlchemyError as e:
        logging.error(f'Error updating inventory item stock: {e}')
        db.rollback()
        return None

def delete_inventory_item(db: Session, inventory_item_id: int):
    try:
        db_inventory_item = db.query(InventoryItem).filter(InventoryItem.id == inventory_item_id).first()
        if not db_inventory_item:
            raise ValueError(f'Inventory Item with id {inventory_item_id} does not exist.')
        db.delete(db_inventory_item)
        db.commit()
        return db_inventory_item
    except SQLAlchemyError as e:
        logging.error(f'Error deleting inventory item: {e}')
        db.rollback()
        return None
