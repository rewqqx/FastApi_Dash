from pydantic import BaseModel


class UserRequest(BaseModel):
    username: str
    password_hashed: str
    role: str
