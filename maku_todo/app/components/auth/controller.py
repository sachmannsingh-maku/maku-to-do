from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import get_db
from .schemas import UserCreate, UserResponse, Token
from .service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate,db: AsyncSession = Depends(get_db)):
    return await register_user(db, user.email, user.password)

@router.post("/login", response_model=Token)
async def login(user: UserCreate,db: AsyncSession = Depends(get_db)):
    return await login_user(db, user.email, user.password)
