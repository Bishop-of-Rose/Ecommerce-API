from typing import Literal
from uuid import uuid7, UUID
from datetime import datetime

from sqlalchemy import func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .carts import Cart

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[Literal['admin', 'customer']] = mapped_column(
        Enum('admin', 'customer', name='user_role'),
        server_default='customer'
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    cart: Mapped['Cart'] = relationship(
        'Cart',
        passive_deletes=True
    )