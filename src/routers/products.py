from typing import List, Literal
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
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
                   category: str = None,
                   price_above: float = None, price_below: float = None,
                   sort: Literal['price_asc', 'price_desc'] = None,
                   page: datetime = None, limit: int = 20):
    limit = max(min(limit, 100), 1)
    stmt = (select(Product)
            .where(Product.name.contains(name))
            .where(Product.description.contains(description))
            .limit(limit))

    if category is not None:
        stmt = stmt.where(Product.category == category)

    if price_above is not None:
        stmt = stmt.where(Product.price < price_above)

    if price_below is not None:
        stmt = stmt.where(Product.price > price_below)

    if page is not None:
        stmt = stmt.where(Product.created_at < page)

    if sort == 'price_asc':
        stmt = stmt.order_by(Product.price.asc())

    else:
        stmt = stmt.order_by(Product.price.desc())

    products = session.scalars(stmt.order_by(Product.created_at.desc())).all()
    page = products[-1].created_at

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

@router.get('/{product_id}', response_model=ProductResponse)
def get_product(product_id: UUID,
                current_user: User = Depends(get_current_admin),
                session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Product not found')

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


