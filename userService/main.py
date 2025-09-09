from fastapi import FastAPI, Response, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from db import users_table
from uuid import uuid4
from models import UserCreate
from botocore.exceptions import BotoCoreError, ClientError

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_path = Path(__file__).parent / "frontend" / "dist"

@app.get("/{user_id}")
async def get_user(user_id: str):

    print("WE AR EGETTING A SINGLE USER")
    print(user_id)

    try:
        response = users_table.get_item(Key={"id": user_id})    
        user = response.get("Item") 

        if user:
            print("User found:", user)
            return {"status": "success", "user": user}

        else:
            print("User not found")
            return {"status": "not_found"}

    except (BotoCoreError, ClientError) as e:
        print("Error fetching user:", e)
        return {"status": "error", "message": str(e)}
    


@app.post("/")
async def create_user(user: UserCreate, response: Response):
    print("IN USER SERVICE")
    user_id = str(uuid4())

    userRow = {
        "id": user_id,
        "name": user.name,
        "email": user.email
    }

    users_table.put_item(Item=userRow)    
    
    print(user_id)
    #response.set_cookie(key="token", value=user_id, httponly=True)
    return {"user_id": user_id}




    





