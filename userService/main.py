from fastapi import FastAPI
from routes.users import router as users_router


app = FastAPI()


app.include_router(users_router)


@app.get("/")
async def intial():
    print("THIS WORKS")

    return "this works"







    





