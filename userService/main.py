from fastapi import FastAPI, Response, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from db import users_table
from uuid import uuid4
from models import UserCreate

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


@app.post("/")
async def create_user(user: UserCreate, response: Response):
    user_id = str(uuid4())

    userRow = {
        "id": user_id,
        "name": user.name,
        "email": user.email
    }

    users_table.put_item(Item=userRow)

    response.set_cookie(
        key="user_id",
        value=user_id,
        httponly=True,     
        secure=False,       
        samesite="lax"      
    )

    print("NEW USER CREATED")

    return Response(status_code=status.HTTP_200_OK)



