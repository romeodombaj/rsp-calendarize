from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from db import users_table
#from routes import route

app = FastAPI()

frontend_path = Path(__file__).parent / "frontend" / "dist"

# serving static files
app.mount("/assets", StaticFiles(directory=frontend_path / "assets"), name="assets")

#app.include_router(route.router, prefix="/route")


@app.get("/api/users")
async def get_users():
    response = users_table.scan()
    return response.get("Items", [])

# serving frontend
@app.get("/{path:path}")
async def serve_react_app(path: str):
    index_file = frontend_path / "index.html"
    return FileResponse(index_file)
