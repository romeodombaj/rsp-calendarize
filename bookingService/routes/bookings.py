
from fastapi import APIRouter, HTTPException
from db import booking_table
from uuid import uuid4
from datetime import datetime
from boto3.dynamodb.conditions import Attr
from models import Booking, BookingList, InputBookInfo
import aiohttp


router = APIRouter(prefix="/bookings", tags=["bookings"])

EMAIL_SERVICE_URL = "http://localhost:5004"

@router.get("/", response_model=BookingList)
async def get_future_appointments():
    try:
        now = datetime.now().isoformat()

        response = booking_table.scan(
            FilterExpression=Attr("date").gte(now)
        )

        future_appointments = response.get("Items", [])

        bookings = [Booking(**item) for item in future_appointments]

        return BookingList(bookings=bookings)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  



@router.patch("/book")
async def book_appointment(booking: InputBookInfo):
    try:
        booking_table.update_item(
            Key={"id": booking.booking_id},
            UpdateExpression="SET #s = :booked_by",
            ExpressionAttributeNames={"#s": "booked_by"},
            ConditionExpression="attribute_not_exists(#s) OR #s = :null_val",
            ExpressionAttributeValues={
                ":booked_by": booking.user_id,
                ":null_val": None  
            },
            ReturnValues="UPDATED_NEW"
        )


        # sending email

        emailData = {
            "user_id": booking.user_id,
            "body": "Hello user, you have booked an appointment",
            "referenceId": booking.booking_id,
            "referenceType": "booking"
        }

        try:
            print("WE ARE SENGIN AN EMAIL")
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{EMAIL_SERVICE_URL}/emails/send", json=emailData) as response:
                    response.raise_for_status()
            
        except Exception as e:
            print("Error Sending Email:", e)

        

        return

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))  




@router.patch("/unbook")
async def book_appointment(booking: InputBookInfo):

    try:
        booking_table.update_item(
            Key={"id": booking.booking_id},
            UpdateExpression="SET #s = :null_value",
            ExpressionAttributeNames={"#s": "booked_by"},
            ExpressionAttributeValues={
                ":null_value": None,                 
                ":expected_user": booking.user_id
            },       
            ConditionExpression="#s = :expected_user",   
            ReturnValues="UPDATED_NEW"
            )
        
        return

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))  




