from pydantic import BaseModel
from datetime import datetime

class Booking(BaseModel):
    id: str
    date: datetime
    name: str
    booked_by: str | None = None

class BookingList(BaseModel):
    bookings: list[Booking]


class InputBookInfo(BaseModel):
    booking_id: str
    user_id: str
