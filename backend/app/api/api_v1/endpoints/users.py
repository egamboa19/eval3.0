from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_users():
    return {"message": "Users endpoint funcionando"}

@router.get("/test")
async def test_users():
    return {"status": "OK", "endpoint": "users"}