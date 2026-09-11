from typing import Set
from uuid import uuid7, UUID
from datetime import datetime

from sqlalchemy import func, ARRAY, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from . import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    categories: Mapped[Set[str]] = mapped_column(ARRAY(String), default=set)
    price: Mapped[float] = mapped_column(nullable=False)
    stock: Mapped[int] = mapped_column(nullable=False)
    image_url: Mapped[str] = mapped_column(default=str)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())