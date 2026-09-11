from typing import List, Set
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import User, Product
from ..schemas import ProductCreate, ProductUpdate, ProductResponse
from ..core.database import get_session
from ..core.dependencies import get_current_user, get_current_admin

router = APIRouter(
    prefix='/products',
    tags=['Products'],
)

@router.get('', response_model=List[ProductResponse])
def query_products(current_user: User = Depends(get_current_user),
                   session: Session = Depends(get_session),
                   name: str = '', description: str = '',
                   categories: Set[str] = None,
                   price_above: float = None, price_below: float = None,
                   page: datetime = None, limit: int = 20):
    stmt = (select(Product)
            .where(Product.name.contains(name))
            .where(Product.description.contains(description))
            .order_by(Product.created_at.desc())
            .limit(limit))

    if page is not None:
        stmt = stmt.where(Product.created_at < page)

    if price_above is not None:
        stmt = stmt.where(Product.price < price_above)

    if price_below is not None:
        stmt = stmt.where(Product.price > price_below)

    if categories is not None:
        stmt = stmt.where(Product.categories.contains(categories))

    products = session.scalars(stmt).all()

    return products

@router.post('', response_model=ProductResponse)
def add_product(product: ProductCreate,
                current_user: User = Depends(get_current_admin),
                session: Session = Depends(get_session)):
    product = Product(**product.model_dump())

    session.add(product)
    session.commit()
    session.refresh(product)

    return product

@router.put('/{product_id}', response_model=ProductResponse)
def update_product(product_id: UUID,
                   edit: ProductUpdate,
                   current_user: User = Depends(get_current_admin),
                   session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Product not found')

    edit = edit.model_dump()
    for key, value in edit.items():
        if edit.get(key) is not None:
            setattr(product, key, value)

    session.commit()
    session.refresh(product)

    return product

@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
def remove_product(product_id: UUID,
                   current_user: User = Depends(get_current_admin),
                   session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Product not found')

    session.delete(product)
    session.commit()

    return


