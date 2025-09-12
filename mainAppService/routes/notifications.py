import requests
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, Request
from models import InputDeleteNotification, OutputCreateNotification, InputCreateNotification
import aiohttp

router = APIRouter(prefix="/notifications", tags=["notifications"])

NOTIFICATION_SERVICE_URL = "http://localhost:5003/notifications/"

@router.post("/")
async def create_notification(inputData: InputCreateNotification):
    try:

        print(inputData)


        print("WE ARE CRETING THE NOTIFICATION")

        async with aiohttp.ClientSession() as session:
            async with session.post(NOTIFICATION_SERVICE_URL, json=inputData.model_dump()) as response:
                response.raise_for_status()
                data = await response.json()
        
        return OutputCreateNotification(notification_id=data["id"], booking_id=data["booking_id"])
            
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e)) 
    
    
@router.delete("/{notification_id}")
async def delete_notification(notification_id: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"{NOTIFICATION_SERVICE_URL}{notification_id}") as response:
                response.raise_for_status()
            
        return

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e)) 


