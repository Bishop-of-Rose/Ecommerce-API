from typing import Literal
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class UserUpdate(BaseModel):
    password: str |  None = None
    first_name: str | None = None
    last_name: str |  None = None

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    role: Literal['admin','customer']
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True