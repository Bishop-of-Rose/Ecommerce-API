from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import update, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

from ..models import User
from ..schemas import UserUpdate, UserResponse
from ..core.database import get_session
from ..core.dependencies import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['Users'],
)

@router.get('/whoami', response_model=UserResponse)
def who_am_i(current_user: User = Depends(get_current_user)):
    return current_user

@router.put('', response_model=UserResponse)
def update_user(edit: UserUpdate,
                current_user: User = Depends(get_current_user),
                session: Session = Depends(get_session)):
    edit = edit.model_dump()
    for key in edit.keys():
        if edit.get(key) is not None:
             setattr(current_user, key, edit[key])

    try:
        session.commit()
        session.refresh(current_user)

    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='User with that email already exists')

    return current_user

@router.delete('', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(current_user: User = Depends(get_current_user),
                session: Session = Depends(get_session)):
    session.delete(current_user)
    session.commit()

    return