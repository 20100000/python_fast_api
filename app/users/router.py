from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.DB.database import get_db
from app.users import schemas
from app.users.services import create, get, update, delete
from app.auth.security import get_current_user
from app.users.models import User as UserModel

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return create.execute(db=db, user=user)  

@router.get("/", response_model=List[schemas.UserResponse])
def read_user(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return get.all_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return get.by_id(db, user_id=user_id)

@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user_data: schemas.UserUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return update.execute(db, user_id=user_id, user_data=user_data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return delete.execute(db, user_id=user_id)

