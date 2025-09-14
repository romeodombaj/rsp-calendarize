from fastapi import FastAPI, Response, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from db import booking_table
from uuid import uuid4
from datetime import datetime
from boto3.dynamodb.conditions import Attr
from routes.bookings import router as bookings_router


app = FastAPI()


app.include_router(bookings_router)


@app.get("/")
async def intial():
    return "Reached Booking Service"

