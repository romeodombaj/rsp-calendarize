from pydantic import BaseModel, EmailStr
from datetime import datetime

class OutputAuthenticate(BaseModel):
    user_id: str


class InputCreateUser(BaseModel):
    name: str
    email: EmailStr

class OutputCreateUser(BaseModel):
    user_id: str


class InputCreateNotification(BaseModel):
    booking_id: str
    booking_time: str              
    user_id: str

class OutputCreateNotification(BaseModel):
    notification_id: str
    booking_id: str

class InputDeleteNotification(BaseModel):
    notification_id: str