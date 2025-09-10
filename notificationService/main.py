from fastapi import FastAPI
from routes.notifications import router as users_router


app = FastAPI()


app.include_router(users_router)






    





