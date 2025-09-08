import requests
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Cookie, HTTPException
from models import UserCreate


router = APIRouter(prefix="/users", tags=["users"])

USER_SERVICE_URL = "http://localhost:5001/"


@router.post("/authenticate")
async def authenticate(user_id: str = Cookie(None)):
    print("CAME TO USERS")

    print(user_id)

    if not user_id:
        print("NO COOKIE")
        raise HTTPException(status_code=400, detail="Missing user_id")

    try:
        response = requests.post(f"{USER_SERVICE_URL}{user_id}")
        response.raise_for_status()
    except requests.RequestException as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

    user_data = response.json()
    user_id = user_data.get("user_id")

    resp = JSONResponse(content={"status": "success", "user_id": user_id})
    
    resp.set_cookie(
        key="user_id",
        value=user_id,
        httponly=True,
        secure=False,  
        samesite="lax"
    )

    return resp

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

    return resp


