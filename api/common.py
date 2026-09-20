from fastapi import APIRouter

router = APIRouter(prefix="", tags=['Main'])

@router.get("/", status_code=200)
async def root():
    return {"message": "Hello"}


@router.get("/health", status_code=200)
async def health():
    return {"status": "ok"}

