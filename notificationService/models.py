from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class InputCreateNotification(BaseModel):
    booking_id: str
    user_id: str
    booking_time: str

class InputDeleteNotification(BaseModel):
    id: str


class NotificationStatus(str, Enum):
    SCHEDULED = "scheduled"
    NOTIFIED = "notified"

class Notification(BaseModel):
    id: str
    booking_id: str
    user_id: str
    status: NotificationStatus
    created_at: datetime
    run_time: datetime



