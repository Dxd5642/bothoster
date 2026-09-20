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

from schemas.auth import RegistrationRequest, LoginRequest, LoginResponse
from redis_client.redis_client import get_redis
from database.connection import get_db
from database.models.users import Users
from core.security import hash_password, verify_password
from core.sessions import generate_session
from api.dependencies import get_current_user

router = APIRouter(prefix="/user", tags=['User'])

@router.get("/")
async def profile_user(user=Depends(get_current_user)):
    return {"user_username": user.username}