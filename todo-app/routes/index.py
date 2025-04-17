from fastapi import APIRouter


router = APIRouter(prefix="/", tags=["index"])


@router.get("/")
async def read_root():
    return {"message": "Welcome to the Todo API!"}
