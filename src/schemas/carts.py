from typing import List
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from .items import ItemResponse

class CartIN(BaseModel):
    items: List[ItemResponse]

class CartOUT(BaseModel):
    user_id: UUID
    items: List[ItemResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True