from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: str
    name: str
    email: EmailStr

class InputCreateUser(BaseModel):
    name: str
    email: EmailStr

class OutputCreateUser(BaseModel):
    id: str



