from enum import Enum
from datetime import datetime
from pydantic import BaseModel, EmailStr

class ReferenceType(str, Enum):
    BOOKING = "booking"
    NOTIFICATION = "notification"


class EmailStatus(str, Enum):
    SENT = "sent"
    RECEIVED = "received"
    FAILED = "failed"


class InputEmailSend(BaseModel):
    user_id: str
    body: str
    referenceId: str
    referenceType: ReferenceType


class EmailLog(BaseModel):
    id: str
    email_id: str
    status: EmailStatus
    email: EmailStr
    referenceId: str
    referenceType: ReferenceType
    createdAt: datetime
