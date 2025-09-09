from pydantic import BaseModel, EmailStr


class OutputAuthenticate(BaseModel):
    user_id: str


class InputCreateUser(BaseModel):
    name: str
    email: EmailStr

class OutputCreateUser(BaseModel):
    user_id: str


    