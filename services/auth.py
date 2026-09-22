import os, re, json
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from database.models.users import Users
from settings.setting import conf

from core.exceptions import *
from schemas.auth import *
from database.models.users import Users
from core.security import hash_password, verify_password
from core.sessions import generate_session
from settings.setting import SESSION_TTL, DEBUG

async def auth_by_username_or_email(db, data):
    pattern = r"^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$"

    user = None

    if re.match(pattern, data):
        user = await Users.get(db, email=data)
    else:
        user = await Users.get(db, username=data)

    return user


async def send_verify_mail(email):
    try:
        message = MessageSchema(
            subject="Subject",
            recipients=[email],
            body="Body",
            subtype=MessageType.html
        )

        fm = FastMail(conf)

        result = await fm.send_message(message=message)

        if result is None:
            return True
        return True
    except:
        raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Server error"
                )


async def login_user_service(
        login: str,
        password: str,
        response: Response,
        db: AsyncSession,
        redis: Redis
):
    login = str(login).strip()
    password = str(password).strip()

    existing_user = await auth_by_username_or_email(db, login)

    if existing_user is None or not verify_password(password, existing_user.password_hash):
       raise InvalidDataForLoginException("Неправильные логин или пароль")

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

    return existing_user


async def register_user_service(
        username: str,
        email: str,
        password: str,
        db: AsyncSession,
):
    username = str(username).strip()
    email = str(email).strip()
    password = str(password).strip()

    existing_user = await Users.get(db, username=username)

    if existing_user:
        raise UserAlreadyExistsException("Пользователь уже зарегистрирован")

    try:
        new_user = await Users.put(db, username=username, email=email, password_hash=hash_password(password))
    except IntegrityError:
        await db.rollback()
        raise UserAlreadyExistsException("Пользователь уже зарегистрирован")

    except:
        raise ServiceException("Ошибка в работе сервера")

    return new_user