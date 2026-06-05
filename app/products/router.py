from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.DB.database import get_db
from app.products import schemas
from app.products.services import create, get, update, delete
from app.auth.security import get_current_user
from app.users.models import User as UserModel

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.post("/", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return create.execute(db=db, product=product)

@router.get("/", response_model=List[schemas.ProductResponse])
def read_product(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return get.all_products(db, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=schemas.ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return get.by_id(db, product_id=product_id)

@router.put("/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, product_data: schemas.ProductUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return update.execute(db, product_id=product_id, product_data=product_data)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return delete.execute(db, product_id=product_id)

