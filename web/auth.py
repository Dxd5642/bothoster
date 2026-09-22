from fastapi import APIRouter, Request, Form, Response, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from core.exceptions import *
from services.auth import *
from redis_client.redis_client import get_redis
from utils.templates import render_template, templates
from database.connection import get_db


router = APIRouter(tags=["Web Auth"])

@router.get("/auth", response_class=HTMLResponse)
async def auth_page(request: Request):
    return await render_template("pages/auth.html", request=request)

@router.get("/login", response_class=HTMLResponse)
async def auth_page(request: Request):
    return await render_template("pages/auth.html", request=request)

@router.get("/registration", response_class=HTMLResponse)
async def auth_page(request: Request):
    return await render_template("pages/auth.html", request=request)


@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis)
):
    try:
        await login_user_service(username, password, response, db, redis)

        response.headers["HX-Redirect"] = "/bots"
        return response

    except InvalidDataForLoginException as e:
        return templates.TemplateResponse(
            request=request,
            name="partials/auth/login_form.html",
            context={"error": e.message},
            status_code=200
        )


@router.post("/registration", response_class=HTMLResponse)
async def register_web(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    if password != confirm_password:
        return templates.TemplateResponse(
            request=request,
            name="partials/auth/register_form.html",
            context={"error": "Пароли не совпадают!"},
            status_code=400
        )

    # TODO Тута еще проверяем чтобы username и email не повторялся

    try:
        await register_user_service(username, email, password, db)

        response = HTMLResponse(content="")
        response.headers["HX-Redirect"] = "/auth?registered=true" # TODO сделать страничку для успешной регистрации
        return response

    except UserAlreadyExistsException as e:
        return templates.TemplateResponse(
            request=request,
            name="partials/auth/register_form.html",
            context={"error": e.message},
            status_code=409
        )

    except ServerErrorException as e:
        return templates.TemplateResponse(
                request=request,
                name="partials/auth/register_form.html",
                context={"error": e.message},
                status_code=500
            )