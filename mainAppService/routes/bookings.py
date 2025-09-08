import requests
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from models import UserCreate


router = APIRouter(prefix="/bookings", tags=["bookings"])

USER_SERVICE_URL = "http://localhost:5001/"


@router.post("/")
async def create_user(user: dict):
    print("CAME TO Bookings")

    user_data = response.json()
    user_id = user_data.get("user_id")

    resp = JSONResponse(content={"status": "success", "user": user_data})
    resp.set_cookie(
        key="user_id",
        value=user_id,
        httponly=True,
        secure=False,  
        samesite="lax"
    )

    return {"user_id": user_id}
