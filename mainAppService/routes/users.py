import requests
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from models import UserCreate


router = APIRouter(prefix="/users", tags=["users"])

USER_SERVICE_URL = "http://localhost:5001/"


@router.post("/")
async def create_user(user: UserCreate):
    print("CAME TO USERS")

    try:
        response = requests.post(USER_SERVICE_URL, json=user.dict())
        response.raise_for_status()
    except requests.RequestException as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

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
