from fastapi import APIRouter

router = APIRouter(prefix="", tags=['API Main'])



@router.get("/health", status_code=200)
async def health():
    return {"status": "ok"}

