
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_route, inventory_item_route, user_route, category_route, stock_location_route
from app.database.database import wait_for_db
from app.database.seeds.seerder import load_seed_data

app = FastAPI(title='SG Inventory FastAPI', version='2.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth_route.router)
app.include_router(user_route.router)
app.include_router(category_route.router)
app.include_router(inventory_item_route.router)
app.include_router(stock_location_route.router)

if __name__ == '__main__': 
    wait_for_db()  
    load_seed_data() 
    uvicorn.run(app, host='0.0.0.0', port=4000)
#python main.py; uvicorn main:app --host 0.0.0.0 --port 4000 --reload