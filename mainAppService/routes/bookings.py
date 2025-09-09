from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import aiohttp


router = APIRouter(prefix="/bookings", tags=["bookings"])


BOOKING_SERVICE_URL = "http://localhost:5002/bookings/"

clients = []

# bookings websocket connection 
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    try:
        async with aiohttp.ClientSession() as session:
                    async with session.get(BOOKING_SERVICE_URL) as response:
                        response.raise_for_status()
                        data = await response.json() 
                        future_bookings = data.get("appointments", [])

            
    except Exception as e:
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

                payload = {
                    "user_id": parsed_data["user_id"],
                    "booking_id": parsed_data["appointment_id"]
                }

                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.patch(f'{BOOKING_SERVICE_URL}book', json=payload) as response:
                            response.raise_for_status()
                            parsedResponse = await response.json()
                    

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

                except Exception as e:
                    print("Error making a booking:", e)

            if parsed_data["type"] == "unbook":

                payload = {
                    "user_id": parsed_data["user_id"],
                    "booking_id": parsed_data["appointment_id"]
                }

                try:
                    

                    async with aiohttp.ClientSession() as session:
                        async with session.patch(f'{BOOKING_SERVICE_URL}unbook', json=payload) as response:
                            response.raise_for_status()
                            parsedResponse = await response.json()

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

                except Exception as e:
                    print("Error removing a booking:", e)

                
            
    except WebSocketDisconnect:
        clients.remove(websocket)
