import requests
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, Request
from models import OutputAuthenticate, InputCreateUser, OutputCreateUser
import aiohttp

router = APIRouter(prefix="/users", tags=["users"])

USER_SERVICE_URL = "http://localhost:5001/users/"


@router.get("/authenticate", response_model=OutputAuthenticate)
async def authenticate(request: Request):
    try:
        user_id = request.cookies.get("user_id")

        if not user_id:
            raise HTTPException(status_code=400, detail="Missing user_id")

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{USER_SERVICE_URL}{user_id}") as response:
                response.raise_for_status()
                user_data = await response.json()

        user_id = user_data.get("id")
        
        return OutputAuthenticate(user_id=user_id)
    
    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) 



@router.post("/", response_model=OutputCreateUser)
async def create_user(user: InputCreateUser):
    try:
        response = requests.post(USER_SERVICE_URL, json=user.model_dump())
        response.raise_for_status()

        async with aiohttp.ClientSession() as session:
            async with session.post(USER_SERVICE_URL, json=user.model_dump()) as response:
                response.raise_for_status()
                user_data = await response.json()
    
        user_id = user_data.get("id")

        resp = JSONResponse(content=OutputCreateUser(user_id=user_id).model_dump())
        
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


