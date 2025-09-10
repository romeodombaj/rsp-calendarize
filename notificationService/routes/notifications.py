from fastapi import APIRouter, HTTPException
from db import notifications_table
from uuid import uuid4
from models import InputCreateNotification, InputDeleteNotification, NotificationStatus, Notification
from datetime import datetime, timedelta


router = APIRouter(prefix="/notifications", tags=["notifications"])




@router.get("/{user_id}")
async def get_user(user_id: str):
    try:
        response = notifications_table.get_item(Key={"id": user_id})    
        user = response.get("Item") 

        if not user:
            raise HTTPException(status_code=404, detail="User not found")    
        
        return

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    


@router.post("/")
async def create_notification(notificationData: InputCreateNotification):
    try:
        id = str(uuid4())

        one_hour_before = datetime(notificationData["booking_time"]) - timedelta(hours=1)

        print(one_hour_before)

        notification_row = Notification(
            id = id,
            user_id = notificationData["user_id"],
            booking_id = notificationData["booking_id"],
            status="scheduled",
            run_time =  one_hour_before,
            created_at = datetime.now()
        )

        
        notification_dict = notification_row.model_dump()
        notification_dict["created_at"] = notification_row.created_at.isoformat()

        notifications_table.put_item(Item=notification_dict)    
        
        return

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))
    

@router.delete("/", )
async def delete_notification(notification: InputDeleteNotification):
    try:

        users_table.delete_item(
            Key={
                "id": notification["id"]
            }
        ) 
        
        return 

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))



