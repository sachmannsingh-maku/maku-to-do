from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import (
    get_user_by_email,
    create_user
)
from .security import hash_password, verify_password, create_access_token

async def register_user(db: AsyncSession, email: str, password: str):
    # 1. Check if user already exists
    existing_user = await get_user_by_email(db, email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # 2. Hash password
    hashed_password = hash_password(password)

    # 3. Create user in DB
    user = await create_user(db, email, hashed_password)

    return user


async def login_user(db: AsyncSession, email: str, password: str):
    # 1. Fetch user
    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # 2. Verify password
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # 3. Create JWT
    token = create_access_token(str(user.id))

    return {
        "access_token": token,
        "token_type": "bearer"
    }
