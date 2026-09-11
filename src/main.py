from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, users,  carts, orders, products

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(carts.router)
app.include_router(orders.router)
app.include_router(products.router)
