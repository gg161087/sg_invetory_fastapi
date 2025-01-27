
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import auth_router, user_router, category_router, product_router, stock_location_router
from src.core.database import wait_for_db
from src.seeders.seerder import load_seed_data

app = FastAPI(title='Stocker FastAPI', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(category_router.router)
app.include_router(product_router.router)
app.include_router(stock_location_router.router)

if __name__ == '__main__': 
    wait_for_db()  
    load_seed_data() 
    uvicorn.run(app, host='0.0.0.0', port=4000)
#python main.py; uvicorn main:app --host 0.0.0.0 --port 4000 --reload