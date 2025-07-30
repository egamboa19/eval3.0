from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_evaluations():
    return {"message": "Evaluations endpoint funcionando"}

@router.get("/test")
async def test_evaluations():
    return {"status": "OK", "endpoint": "evaluations"}