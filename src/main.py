from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse

from .routers import auth, users, carts, items, orders, products

app = FastAPI()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=['50/minute']
)

app.state.limiter = limiter
@app.exception_handler(RateLimitExceeded)
def rate_limit_exceeded_handler(exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        headers={"Retry-After": exc.detail},
        content={"detail": "Rate limit exceeded"}
    )

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
