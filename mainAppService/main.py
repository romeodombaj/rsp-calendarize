from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from db import users_table
from uuid import uuid4
from routes.users import router as users_router
import requests
import json


app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(users_router, prefix="/api")


BOOKING_SERVICE_URL = "http://localhost:5002/"

clients = []

# bookings websocket connection 
@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):

    # dohvaca se cookie "user_id"
    #user_id = websocket.cookies.get("user_id")

    # ako cookie ne postoji generira se novi used id i salje koriniku u obliku httpOnly cookiea
    #if not user_id:
     #   user_id = str(uuid4())
      #  await websocket.accept(headers=[("Set-Cookie", f"user_id={user_id}; Path=/; HttpOnly; SameSite=None; ")])
       # print("New Client Connected")
   # else:
    #    print("Existing Client Connected")


    await websocket.accept()

    try:
        response = requests.get(BOOKING_SERVICE_URL)
        response.raise_for_status()
        future_bookings = response.json().get("appointments", [])
    except requests.RequestException as e:
        future_bookings = []
        print("Error fetching bookings:", e)

    await websocket.send_text(json.dumps({
        "type": "all_bookings",
        "data": future_bookings
    }))
        
    clients.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            parsed_data = json.loads(data)

            if parsed_data["type"] == "book":
                print("This is new booking")

                payload = {
                    "user_id": parsed_data["user_id"],
                    "booking_id": parsed_data["appointment_id"]
                }

                print(payload)

                try:
                    response = requests.put(f'{BOOKING_SERVICE_URL}book', json=payload)
                    response.raise_for_status()
                    
                    parsedResponse = response.json()

                    if parsedResponse["status"] == "error":
                        await websocket.send_text(json.dumps({
                            "type": "error",
                            "message": parsedResponse.get("message", "Unknown error")
                        }))
                        continue


                    updateData = {
                        "booked_by": parsed_data["user_id"],
                        "appointment_id": parsed_data["appointment_id"],
                        "type": "new_booking"
                    }


                    for client in clients:
                        await client.send_text(json.dumps(updateData))

                except requests.RequestException as e:
                    print("Error fetching bookings:", e)

            if parsed_data["type"] == "unbook":

                payload = {
                    "user_id": parsed_data["user_id"],
                    "booking_id": parsed_data["appointment_id"]
                }

                try:
                    response = requests.put(f'{BOOKING_SERVICE_URL}unbook', json=payload)
                    response.raise_for_status()
                    print("RESPONSE RECEIVED")

                    parsedResponse = response.json()

                    print(parsedResponse)
                    print(parsedResponse["status"])
                    print(parsedResponse["status"] == "error")

                    if parsedResponse["status"] == "error":
                        await websocket.send_text(json.dumps({
                            "type": "error",
                            "message": parsedResponse.get("message", "Unknown error")
                        }))
                        continue
                    
                    updateData = {
                        "booked_by": None,
                        "appointment_id": parsed_data["appointment_id"],
                        "type": "canceled_booking"
                    }

                    for client in clients:
                        await client.send_text(json.dumps(updateData))

                except requests.RequestException as e:
                    print("Error fetching bookings:", e)

                
            
    except WebSocketDisconnect:
        clients.remove(websocket)



# serving frontend
frontend_path = Path(__file__).parent / "frontend" / "dist"

app.mount("/assets", StaticFiles(directory=frontend_path / "assets"), name="assets")

@app.get("/{path:path}")
async def serve_react_app(path: str):
    index_file = frontend_path / "index.html"
    return FileResponse(index_file)
