from fastapi import (
    APIRouter, 
    Request, 
    Response, 
    Depends, 
    HTTPException,
    status)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
import json

from redis.asyncio import Redis

from schemas.auth import *
from redis_client.redis_client import get_redis
from database.connection import get_db
from database.models.users import Users
from core.security import hash_password, verify_password
from core.sessions import generate_session
from api.dependencies import get_current_user
from services.auth import *
from settings.setting import DEBUG, SESSION_TTL


router = APIRouter(prefix="/v1/auth", tags=['API Auth'])


@router.post("/registration", status_code=status.HTTP_201_CREATED)
async def registration_user(
    data: RegistrationRequest, 
    db: AsyncSession = Depends(get_db)
    ):

    try: # TODO Сделать RegisterResponse
        result = await register_user_service(data.username, data.email, data.password, db)
        return {"status": result is not None, "data": result}

    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message
        )

    except ServiceException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message
        )


@router.post("/login", response_model=LoginResponse, status_code=200)
async def login_user(
    data: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis)
):
    try:
        user = await login_user_service(data.login, data.password, response, db, redis)
        return LoginResponse(username=user.username, email=user.email)
    except InvalidDataForLoginException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message
        )


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    redis: Redis = Depends(get_redis),
):
    session_id = request.cookies.get("session_id")

    if session_id:
        await redis.delete(f"session:{session_id}")

    response.delete_cookie(
        key="session_id",
        path="/",
        httponly=True,
        secure=not DEBUG,
        samesite="lax",
    )

    return {"message": "Logged out successfully"}


@router.get("/me", response_model=MeResponse, status_code=200)
async def me(user: Users = Depends(get_current_user)):
    return {"username": user.username, "email": user.email}


@router.post("/verify-email", response_model=None, status_code=200)
async def verify_email(data: VeriryEmailRequest, db = Depends(get_db)):
    email = str(data.email).strip()
    existing_user = await auth_by_username_or_email(db, email)

    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid user"
        )

    # TODO Здесь будет генерировать токен, и сохранять его в Redis под verify-token:{token}:user_id

    result = await send_verify_mail(existing_user.email)
    if result is None or result is False:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Server error"
        )

    return {"status": True, "message": "Письмо на почту отправлено"}
