from uuid import UUID, uuid7
from datetime import datetime

from sqlalchemy import func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .products import Product

class Item(Base):
    __tablename__ = "items"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    cart_id: Mapped[UUID] = mapped_column(ForeignKey('carts.id', ondelete='CASCADE', name='fk_item_cart'), nullable=False)
    product_id: Mapped[UUID] = mapped_column(ForeignKey('products.id', ondelete='CASCADE', name='fk_item_product'), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    product: Mapped['Product'] = relationship('Product')

    __table_args__ = (
        UniqueConstraint('cart_id', 'product_id', name='uq_item_cart_product'),
    )