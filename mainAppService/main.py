from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from db import users_table
from uuid import uuid4
from routes.users import router as users_router

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

# serving static files
app.mount("/assets", StaticFiles(directory=frontend_path / "assets"), name="assets")

app.include_router(users_router, prefix="/api")


clients = []

# bookings websocket connection 
@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):

    # dohvaca se cookie "user_id"
    user_id = websocket.cookies.get("user_id")

    # ako cookie ne postoji generira se novi used id i salje koriniku u obliku httpOnly cookiea
    if not user_id:
        user_id = str(uuid4())
        await websocket.accept(headers=[("Set-Cookie", f"user_id={user_id}; Path=/; HttpOnly; SameSite=None; ")])
        print("New Client Connected")
    else:
        await websocket.accept()
        print("Existing Client Connected")


    clients.append(websocket)

    #print("New Client: ", websocket)
    
    try:
        while True:
            data = await websocket.receive_text()

            for client in clients:
                await client.send_text(data)
    except WebSocketDisconnect:
        clients.remove(websocket)



#@app.get("/api/users")
#async def get_users():
 #   response = users_table.scan()
  #  return response.get("Items", [])

# serving frontend
@app.get("/{path:path}")
async def serve_react_app(path: str):
    index_file = frontend_path / "index.html"
    return FileResponse(index_file)
