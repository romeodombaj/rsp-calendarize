from fastapi import APIRouter, HTTPException
from models import UserCreate
from db import users_table
from uuid import uuid4
from models import UserCreate

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}")
async def get_user(user_id: str):
    try:
        response = users_table.get_item(Key={"id": user_id})    
        user = response.get("Item") 

        if not user:
            raise HTTPException(status_code=404, detail="User not found")    
        
        return {"status": "success", "user": user}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    


@router.post("/")
async def create_user(user: UserCreate):
    try:
        user_id = str(uuid4())

        userRow = {
            "id": user_id,
            "name": user.name,
            "email": user.email
        }

        users_table.put_item(Item=userRow)    
        
        return {"user_id": user_id}

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))



