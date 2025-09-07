from pydantic import BaseModel, EmailStr
import uuid

class UserCreate(BaseModel):
    id: str = str(uuid.uuid4()) 
    name: str
    email: EmailStr
