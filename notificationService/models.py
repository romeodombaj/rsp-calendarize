from pydantic import BaseModel, EmailStr
from datetime import datetime

class InputCreateNotification(BaseModel):
    booking_id: str
    user_id: str
    booking_time: datetime

class InputDeleteNotification(BaseModel):
    id: str


class NotificationStatus(BaseModel):
    SCHEDULED = "scheduled"
    NOTIFIED = "notified"

class Notification(BaseModel):
    id: str
    booking_id: str
    user_id: str
    status: NotificationStatus
    created_at: datetime
    run_time: datetime

