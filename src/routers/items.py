from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation, ForeignKeyViolation

from ..models import User, Item
from ..schemas import CartOUT, ItemCreate, ItemUpdate
from ..core.database import get_session
from ..core.dependencies import get_current_customer

router = APIRouter(
    prefix='/items',
    tags=['Items'],
)

@router.post('', response_model=CartOUT)
def add_items(items: List[ItemCreate],
              current_user: User = Depends(get_current_customer),
              session: Session = Depends(get_session)):
    if current_user.cart is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Cart not found')

    items = [Item(**item.model_dump(), cart_id=current_user.cart.id) for item in items]
    try:
        current_user.cart.items.append(*items)
        session.commit()

    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Some added items already exists')

        if isinstance(e.orig, ForeignKeyViolation):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Some referred products do not exist')

    return current_user.cart

@router.put('', response_model=CartOUT)
def update_items(items: List[ItemUpdate],
                 current_user: User = Depends(get_current_customer),
                 session: Session = Depends(get_session)):
    if current_user.cart is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Cart not found')

    new_items = [item.model_dump() for item in items]
    old_items = [ItemUpdate.model_validate(item, from_attributes=True).model_dump() for item in current_user.cart.items]

    new_products = set([str(item.product_id) for item in new_items])
    old_products = set([str(item.product_id) for item in old_items])

    difference = new_products.symmetric_difference(old_products)
    if len(difference) > 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Some specified items do not exist')

@router.delete('', response_model=CartOUT)
def remove_items(items: List[UUID],
                 current_user: User = Depends(get_current_customer),
                 session: Session = Depends(get_session)):
    pass