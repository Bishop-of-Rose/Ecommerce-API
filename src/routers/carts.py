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
def get_cart(current_user: User = Depends(get_current_customer),
             session: Session = Depends(get_session)):
    if current_user.cart is None:
        cart = Cart(user_id=current_user.id)
        session.add(cart)
        session.commit()

    return current_user.cart

@router.put('', response_model=CartOUT)
def save_cart(edit: CartIN,
              current_user: User = Depends(get_current_customer),
              session: Session = Depends(get_session)):
    if current_user.cart is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Cart not found')

    items = [Item(**item.model_dump()) for item in edit.items]
    current_user.cart.items = items

    session.commit()
    return current_user.cart

@router.head('/checkout', response_model=CartOUT)
def checkout_cart(current_user: User = Depends(get_current_customer),
                  session: Session = Depends(get_session)):
    if current_user.cart is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Cart not found')

    pass