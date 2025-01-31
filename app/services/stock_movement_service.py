from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.stock_movement_model import StockMovement
from app.models.inventory_item_model import Product
from app.models.stock_location_model import StockLocation
import logging

def create_stock_movement(db: Session, product_id: int, stock_location_id: int, movement_type: str, quantity: int, reason: str):
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError(f'Product with id {product_id} does not exist.')
        if stock_location_id:
            stock_location = db.query(StockLocation).filter(StockLocation.id == stock_location_id).first()
            if not stock_location:
                raise ValueError(f'Stock location with id {stock_location_id} does not exist.')
        if movement_type == "exit" and (product.current_stock is None or product.current_stock < quantity):
            raise ValueError('Not enough stock available.')
        stock_movement = StockMovement(
            product_id=product_id,
            stock_location_id=stock_location_id,
            movement_type=movement_type,
            quantity=quantity,
            reason=reason
        )
        db.add(stock_movement)
        if movement_type == "entry":
            if product.current_stock is None:
                product.current_stock = 0
            product.current_stock += quantity
        elif movement_type == "exit":
            if product.current_stock is None or product.current_stock < quantity:
                raise ValueError("Insufficient stock")
            product.current_stock -= quantity
        db.commit()
        db.refresh(product)
        db.refresh(stock_movement)

        return stock_movement
    except SQLAlchemyError as e:
        logging.error(f'Error creating stock movement: {e}')
        db.rollback()
        return None