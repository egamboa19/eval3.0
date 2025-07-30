from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_surveys():
    return {"message": "Surveys endpoint funcionando"}

@router.get("/test")
async def test_surveys():
    return {"status": "OK", "endpoint": "surveys"}