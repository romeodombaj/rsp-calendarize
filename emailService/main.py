from fastapi import FastAPI
from routes.emails import router as emails_router

app = FastAPI()

app.include_router(emails_router)






