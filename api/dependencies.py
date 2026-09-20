from fastapi import Depends, HTTPException, Request, status
import redis.asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession
import json


from redis_client.redis_client import get_redis
from database.connection import get_db
from database.models.users import Users

async def get_current_user(
        request: Request, 
        redis: aioredis.Redis = Depends(get_redis),
        db: AsyncSession = Depends(get_db)
    ):
    session_id = request.cookies.get("session_id")

    if not session_id:
        raise HTTPException(
            status_code=401,
            detail="Not authentificated"
        )

    session_data =json.loads(await redis.get(f"session:{session_id}"))

    if session_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired"
        )

    user = await Users.get(db, id=session_data.get("user_id"))

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid user",
        )
    
    return user

