from uuid import UUID
from datetime import datetime

from pydantic import BaseModel
from .products import ProductResponse

class ItemCreate(BaseModel):
    product_id: UUID
    quantity: int

class ItemUpdate(BaseModel):
    product_id: UUID
    quantity: int

class ItemResponse(BaseModel):
    id: UUID
    product: ProductResponse
    quantity: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True