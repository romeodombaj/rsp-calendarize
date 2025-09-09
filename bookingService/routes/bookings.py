
from fastapi import Response, APIRouter, HTTPException
from db import booking_table
from uuid import uuid4
from datetime import datetime
from boto3.dynamodb.conditions import Attr



router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("/")
async def get_future_appointments():
    try:
        now = datetime.now().isoformat()

        response = booking_table.scan(
            FilterExpression=Attr("date").gte(now)
        )

        future_appointments = response.get("Items", [])

        return {"appointments": future_appointments}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  



@router.patch("/book")
async def book_appointment(booking: dict, response: Response):
    try:
        booking_table.update_item(
            Key={"id": booking["booking_id"]},
            UpdateExpression="SET #s = :booked_by",
            ExpressionAttributeNames={"#s": "booked_by"},
            ConditionExpression="attribute_not_exists(#s) OR #s = :null_val",
            ExpressionAttributeValues={
                ":booked_by": booking["user_id"],
                ":null_val": None  
            },
            ReturnValues="UPDATED_NEW"
        )

        return {"status": "success"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  




@router.patch("/unbook")
async def book_appointment(booking: dict, response: Response):

    try:
        booking_table.update_item(
            Key={"id": booking["booking_id"]},
            UpdateExpression="SET #s = :null_value",
            ExpressionAttributeNames={"#s": "booked_by"},
            ExpressionAttributeValues={
                ":null_value": None,                 
                ":expected_user": booking["user_id"]
            },       
            ConditionExpression="#s = :expected_user",   
            ReturnValues="UPDATED_NEW"
            )
        
        return {"status": "success"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  




