from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from utils.templates import render_template

from web.home import router as home_router
from web.auth import router as auth_router

router = APIRouter(tags=["Web Pages"])

router.include_router(home_router)
router.include_router(auth_router)