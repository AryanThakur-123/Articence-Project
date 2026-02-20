
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/")
def root():
    return JSONResponse(content={"message": "Welcome to the Universal Data Connector API!"})

@router.get("/test")
def test():
    print("Hello")
    return "OK"
