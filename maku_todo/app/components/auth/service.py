from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from .exceptions import InvalidEmailFormat
from maku_todo.tasks.email import send_welcome_email
logger = logging.getLogger("auth")

from .repository import (
    get_user_by_email,
    create_user
)
from .security import hash_password, verify_password, create_access_token

async def register_user(db: AsyncSession, email: str, password: str):
    try:
        if '@' not in email:
            raise InvalidEmailFormat()
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
        send_welcome_email.delay(user.email)
        return user
    
    except InvalidEmailFormat:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Specified Email '{email}' is not of the correct format"
        )


async def login_user(db: AsyncSession, email: str, password: str):
    # 1. Fetch user
    user = await get_user_by_email(db, email)
    if not user:
        logger.warning(f'event=login_failed email : {email}')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    if isinstance(user, str):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=user
        )
    # 2. Verify password
    if not verify_password(password, user.hashed_password):
        logger.warning(f'event=login_failed email : email')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # 3. Create JWT
    token = create_access_token(str(user.id))

    logger.info(f"event=login user_id={user.id} email={user.email}")

    return {
        "access_token": token,
        "token_type": "bearer"
    }
