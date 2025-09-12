from fastapi import APIRouter, HTTPException
from db import notifications_table
from uuid import uuid4
from models import InputCreateNotification, InputDeleteNotification, NotificationStatus, Notification
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key


router = APIRouter(prefix="/notifications", tags=["notifications"])



@router.get("/user/{user_id}")
async def get_notifications_by_user_id(user_id: str):
    try:
        response = notifications_table.scan(
        FilterExpression=Key("user_id").eq(user_id)
)    
        
        notifications = response.get("Items", [])
        
        return notifications

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))    


@router.post("/")
async def create_notification(notificationData: InputCreateNotification):
    try:
        id = str(uuid4())


        booking_time = datetime.fromisoformat(notificationData.booking_time.replace("Z", "+00:00"))
        one_hour_before = booking_time - timedelta(hours=1)

        print(one_hour_before)

        notification_row = Notification(
            id = id,
            user_id = notificationData.user_id,
            booking_id = notificationData.booking_id,
            status="scheduled",
            run_time =  one_hour_before,
            created_at = datetime.now()
        )

        
        notification_dict = notification_row.model_dump()
        notification_dict["created_at"] = notification_row.created_at.isoformat()
        notification_dict["run_time"] = notification_row.run_time.isoformat()

        notifications_table.put_item(Item=notification_dict)    
        
        return notification_dict

    except Exception as e:
        print(notificationData)
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))
    

@router.delete("/{notification_id}")
async def delete_notification(notification_id: str):
    try:

        notifications_table.delete_item(
            Key={
                "id": notification_id
            }
        ) 
        
        return 

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))



