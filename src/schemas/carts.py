from typing import List
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from .items import ItemResponse

class CartResponse(BaseModel):
    id: UUID
    user_id: UUID
    items: List[ItemResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True