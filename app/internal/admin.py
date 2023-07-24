from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def admin():
    return {"message": "admin Site"}


@router.post("/")
async def update_admin():
    return {"message": "admin getting schwifty"}
