from fastapi import HTTPException, status
from app.config.dependency import db_dependency, user_dependency
from app.schemas.inventory_item_schema import InventoryItemCreate, InventoryItemUpdate
from app.services import inventory_item_service
from app.auth.jwt_handler import check_user
import logging

def get_inventory_item(inventory_item_id: int, db: db_dependency, user: user_dependency):
    check_user(user)
    try:
        db_inventory_item = inventory_item_service.read_inventory_item(db, inventory_item_id)
        if db_inventory_item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Inventory Item not found')
        return db_inventory_item
    except Exception as e:
        logging.error(f'Error reading inventory item: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')
    
def get_inventory_items(user: user_dependency, db: db_dependency, skip: int, limit: int):
    check_user(user)
    try:
        inventory_items = inventory_item_service.read_inventory_items(db, skip=skip, limit=limit)
        return inventory_items
    except Exception as e:
        logging.error(f'Error reading inventory items: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')
    
def create_inventory_item(inventory_item_data: InventoryItemCreate, db: db_dependency, user: user_dependency):
    check_user(user)
    if inventory_item_service.read_inventory_item_by_sku(db, inventory_item_data.sku):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Inventory Item with SKU {inventory_item_data.sku} already exists')
    new_inventory_item = inventory_item_service.create_inventory_item(db, inventory_item_data)
    if not new_inventory_item:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to create inventory item')
    return new_inventory_item

def update_inventory_item(inventory_item_id: int, inventory_item_data: InventoryItemUpdate, db: db_dependency, user: user_dependency):
    check_user(user)
    try:
        db_inventory_item = inventory_item_service.update_inventory_item(db, inventory_item_id, inventory_item_data)
        if db_inventory_item is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error updating inventory_item')
        return db_inventory_item
    except Exception as e:
        logging.error(f'Error updating inventory item: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')
    
def update_inventory_item_stock(inventory_item_id: int, quantity: int, db: db_dependency, user: user_dependency):
    check_user(user)
    try:
        updated_inventory_item = inventory_item_service.update_inventory_item_stock(db, inventory_item_id, quantity)
        if not updated_inventory_item:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Inventory Item not found')
        return updated_inventory_item
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')

def delete_inventory_item(inventory_item_id: int, db: db_dependency, user: user_dependency):
    check_user(user)
    try:
        db_inventory_item = inventory_item_service.delete_inventory_item(db, inventory_item_id)
        if db_inventory_item is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error deleting inventory item')
        return db_inventory_item
    except Exception as e:
        logging.error(f'Error deleting inventory item: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')