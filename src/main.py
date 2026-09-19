from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, users, carts, items, orders, products
from .core.limiter import limiter, RateLimitExceeded, rate_limit_exceeded_handler

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

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
app.include_router(items.router)
app.include_router(orders.router)
app.include_router(products.router)

@app.get('/')
def root():
    return {'message': 'Hello World'}
