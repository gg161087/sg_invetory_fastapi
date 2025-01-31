from fastapi import HTTPException, status
from app.schemas.stock_movement_schema import StockMovementCreate
from app.config.dependency import db_dependency, user_dependency
from app.services import stock_movement_service
import logging

def create_stock_movement(stock_movement: StockMovementCreate, db: db_dependency, user: user_dependency):
    try:
        new_stock_movement = stock_movement_service.create_stock_movement(
            db,
            stock_movement.product_id,
            stock_movement.stock_location_id,
            stock_movement.movement_type,
            stock_movement.quantity,
            stock_movement.reason
        )
        if not new_stock_movement:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating stock movement")
        return new_stock_movement
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logging.error(f'Error creating stock movement: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')
