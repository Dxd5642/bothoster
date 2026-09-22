from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from utils.templates import render_template

router = APIRouter(tags=["Web Home"])

@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return await render_template("pages/index.html", request=request)