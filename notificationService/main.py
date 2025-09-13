from fastapi import FastAPI
from routes.notifications import router as users_router
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
import asyncio
from services.triggerNotificationService import check_and_send_notifications

app = FastAPI()
scheduler = BackgroundScheduler()



app.include_router(users_router)


@app.on_event("startup")
async def start_scheduler():
    print("SCHEDULER STARTED")
    scheduler.add_job(lambda: asyncio.run(check_and_send_notifications()), 'interval', seconds=5)
    scheduler.start()

@app.on_event("shutdown")
def shutdown_scheduler():
    print("SCHEDULER ENDED")
    scheduler.shutdown()



    





