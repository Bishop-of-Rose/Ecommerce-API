from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..models import User, Cart, Item
from ..schemas import CartIN, CartOUT
from ..core.database import get_session
from ..core.dependencies import get_current_customer
router = APIRouter(
    prefix='/carts',
    tags=['Carts'],
)

@router.get('', response_model=CartOUT)
def get_cart(current_user: User = Depends(get_current_customer)):
    return current_user.cart

@router.put('', response_model=CartOUT)
def save_cart(edit: CartIN,
              current_user: User = Depends(get_current_customer),
              session: Session = Depends(get_session)):
    items = [Item(**item.model_dump()) for item in edit.items]
    current_user.cart.items = items

    session.commit()
    session.refresh(current_user.cart)
    return current_user.cart

@router.delete('')
def empty_cart(current_user: User = Depends(get_current_customer),
               session: Session = Depends(get_session)):
    current_user.cart.items = []

    session.commit()
    return

@router.head('/checkout', response_model=CartOUT)
def checkout_cart(current_user: User = Depends(get_current_customer),
                  session: Session = Depends(get_session)):
    pass