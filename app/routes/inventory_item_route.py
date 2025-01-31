from fastapi import APIRouter, status
from typing import List
from app.config.dependency import db_dependency, user_dependency
from app.schemas.inventory_item_schema import InventoryItemCreate, InventoryItemUpdate, InventoryItemResponse
from app.controllers import inventory_item_controller

router = APIRouter(prefix='/inventory_items', tags=['Inventory Items'])

@router.get('/{inventory_item_id}', summary='GET Inventory Item by ID', response_model=InventoryItemResponse)
def get_inventory_item(inventory_item_id: int, db: db_dependency, user: user_dependency):
    return inventory_item_controller.get_inventory_item(inventory_item_id, db, user)
    
@router.get('/', summary='GET ALL Inventory Items', response_model=List[InventoryItemResponse], status_code=status.HTTP_200_OK)
def get_inventory_items(user: user_dependency, db: db_dependency, skip: int = 0, limit: int = 100):
    return inventory_item_controller.get_inventory_items(user, db, skip, limit)
    
@router.post('/', summary='CREATE new Inventory Item', status_code=status.HTTP_201_CREATED)
def create_product(inventory_item_data: InventoryItemCreate, db: db_dependency, user: user_dependency):
    return inventory_item_controller.create_product(inventory_item_data, db, user)

@router.put('/{inventory_item_id}', summary='UPDATE Inventory Item by ID', response_model=InventoryItemResponse)
def update_inventory_item(inventory_item_id: int, inventory_item_data: InventoryItemUpdate, db: db_dependency, user: user_dependency):
    return inventory_item_controller.update_inventory_item(inventory_item_id, inventory_item_data, db, user)
    
@router.put('/stock/{inventory_item_id}', summary='UPDATE Inventory Item Stock', status_code=status.HTTP_200_OK)
def update_inventory_item_stock(inventory_item_id: int, quantity: int, db: db_dependency, user: user_dependency):
    return inventory_item_controller.update_inventory_item_stock(inventory_item_id, quantity, db, user)

@router.delete('/{inventory_item_id}', summary='DELETE Inventory Item by ID', response_model=InventoryItemResponse)
def delete_inventory_item(inventory_item_id: int, db: db_dependency, user: user_dependency):
    return inventory_item_controller.delete_inventory_item(inventory_item_id, db, user)