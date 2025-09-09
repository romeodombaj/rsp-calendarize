import requests
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, Request
from models import UserCreate
import aiohttp

router = APIRouter(prefix="/users", tags=["users"])

USER_SERVICE_URL = "http://localhost:5001/users/"


@router.get("/authenticate")
async def authenticate(request: Request):
    try:
        user_id = request.cookies.get("user_id")

        if not user_id:
            raise HTTPException(status_code=400, detail="Missing user_id")

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{USER_SERVICE_URL}{user_id}") as response:
                response.raise_for_status()
                user_data = await response.json()


        user_id = user_data.get("user", {}).get("id") 
        
        return {"status": "success", "user_id": user_id}
    
    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) 



@router.post("/")
async def create_user(user: UserCreate):
    try:
        response = requests.post(USER_SERVICE_URL, json=user.dict())
        response.raise_for_status()

        async with aiohttp.ClientSession() as session:
            async with session.post(USER_SERVICE_URL, json=user.dict()) as response:
                response.raise_for_status()
                user_data = await response.json()
    
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

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e)) 


