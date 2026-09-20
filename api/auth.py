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

from schemas.auth import RegistrationRequest, LoginRequest, LoginResponse, MeResponse
from redis_client.redis_client import get_redis
from database.connection import get_db
from database.models.users import Users
from core.security import hash_password, verify_password
from core.sessions import generate_session
from api.dependencies import get_current_user
from settings.setting import DEBUG

router = APIRouter(prefix="/auth", tags=['Auth'])

SESSION_TTL = 60 * 60 # 1 час


@router.post("/registration", status_code=status.HTTP_201_CREATED)
async def registration_user(
    data: RegistrationRequest, 
    db: AsyncSession = Depends(get_db)
    ):

    email = str(data.email).strip()
    username = str(data.username).strip()
    password = str(data.password).strip()

    existing_user = await Users.get(db, username=username)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already registered",
        )

    try:
        result = await Users.put(db, username=username, email=email, password_hash=hash_password(password))
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already registered"
            )

    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
            )

    return {"status": result}

    

@router.post("/login", response_model=LoginResponse, status_code=200)
async def login_user(
    data: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis)
):
    username = str(data.username).strip()
    password = str(data.password).strip()

    existing_user = await Users.get(db, username=username)

    if existing_user is None or not verify_password(password, existing_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    session_id = await generate_session()

    session_date = {
        "user_id": str(existing_user.id),
    }

    await redis.set(
        f"session:{session_id}",
        json.dumps(session_date),
        ex=SESSION_TTL
    )

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=not DEBUG,
        samesite="lax",
        max_age=SESSION_TTL,
        path="/",
    )

    return LoginResponse(username=username, email=existing_user.email)

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
