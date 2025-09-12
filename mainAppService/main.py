from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from routes.users import router as users_router
from routes.bookings import router as bookings_router
from routes.notifications import router as notifications_routes


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
app.include_router(bookings_router, prefix="/api")
app.include_router(notifications_routes, prefix="/api")



# serving frontend
frontend_path = Path(__file__).parent / "frontend" / "dist"

app.mount("/assets", StaticFiles(directory=frontend_path / "assets"), name="assets")

@app.get("/{path:path}")
async def serve_react_app(path: str):
    index_file = frontend_path / "index.html"
    return FileResponse(index_file)
