from typing import Literal
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

class UserUpdate(BaseModel):
    email: str | None = None
    password: str |  None = None
    first_name: str | None = None
    last_name: str |  None = None

class UserResponse(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    role: Literal['admin','customer']
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True