from typing import Set
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str
    category: str
    price: float
    stock: int
    image_url: str | None = None

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    price: float | None = None
    stock: int | None = None
    image_url: str | None = None

class ProductResponse(BaseModel):
    id: UUID
    name: str
    description: str
    category: str
    price: float
    stock: int
    image_url: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True