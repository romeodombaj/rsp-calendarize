from fastapi import FastAPI, Response, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from db import booking_table
from uuid import uuid4
from datetime import datetime
from boto3.dynamodb.conditions import Attr


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

@app.get("/")
async def get_future_appointments():
    now = datetime.now().isoformat()

    print("CURRENT TIME ", now)

    response = booking_table.scan(
            FilterExpression=Attr("date").gte(now)

    )

    future_appointments = response.get("Items", [])

    return {"appointments": future_appointments}



@app.put("/book")
async def book_appointment(booking: dict, response: Response):
    print("IN Booking SERVICE")

    print(booking)
    try:
        booking_table.update_item(
            Key={"id": booking.booking_id},
            UpdateExpression="SET #s = :booked_by", 
            ExpressionAttributeNames={"#s": "booked_by"},  
            ExpressionAttributeValues={":booked_by": booking.user_id},
            ReturnValues="UPDATED_NEW"  
        )
    except Exception as e:
        print("Error updating user:", e)
        return {"status": "error", "message": str(e)}

    return {"status": "success"}





