from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.DB.database import get_async_db
from app.api.users import schemas
from app.api.users.v2.services import update, create, get, delete
from app.auth.security import get_current_user
from app.api.users.models import User as UserModel

router = APIRouter(
    prefix="/v2/users",
    tags=["users v2 (Async"]
)

@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_v2(user: schemas.UserCreate, db: AsyncSession = Depends(get_async_db)):
    return await create.execute(db=db, user=user)

@router.get("/", response_model=List[schemas.UserResponse])
async def read_user_v2(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_db), current_user: UserModel = Depends(get_current_user)):
    return await get.all_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=schemas.UserResponse)
async def read_user_v2(user_id: int, db: AsyncSession = Depends(get_async_db), current_user: UserModel = Depends(get_current_user)):
    return await get.by_id(db, user_id=user_id)

@router.put("/{user_id}", response_model=schemas.UserResponse)
async def update_user_v2(user_id: int, user_data: schemas.UserUpdate, db: AsyncSession = Depends(get_async_db), current_user: UserModel = Depends(get_current_user)):
    return await update.execute(db, user_id=user_id, user_data=user_data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_v2(user_id: int, db: AsyncSession = Depends(get_async_db), current_user: UserModel = Depends(get_current_user)):
    return await delete.execute(db, user_id=user_id)

