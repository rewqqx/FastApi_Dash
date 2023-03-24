from pydantic import BaseModel
from datetime import datetime


class UserResponse(BaseModel):
    id: int
    username: str
    password_hashed: str
    role: str
    created_at: datetime

    class Config:
        orm_mode = True
