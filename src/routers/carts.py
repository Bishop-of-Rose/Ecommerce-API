from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import User, Cart, Item, Product
from ..schemas import CartResponse, ItemCreate, ItemUpdate
from ..core.database import get_session
from ..core.dependencies import get_current_customer
router = APIRouter(
    prefix='/carts',
    tags=['Carts'],
)

@router.get('', response_model=CartResponse)
def get_or_add_cart(current_user: User = Depends(get_current_customer),
                    session: Session = Depends(get_session)):
    stmt = select(Cart).where(Cart.user_id == current_user.id)
    cart = session.scalars(stmt).one_or_none()

    if cart is None:
        cart = Cart(user_id = current_user.id)
        session.add(cart)
        session.commit()
        session.refresh(cart)

    return cart

@router.post('', response_model=CartResponse)
def add_items(items: List[ItemCreate],
              current_user =  Depends(get_current_customer),
              session: Session = Depends(get_session)):
    stmt = select(Cart).where(Cart.user_id == current_user.id)
    cart = session.scalars(stmt).one_or_none()

    if cart is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Cart not found')

    old_items = [ItemCreate.model_validate(item).model_dump() for item in cart.items]
    new_items = [item.model_dump() for item in items]

    print(old_items)
    print(new_items)

    return