from pydantic import BaseModel


class JwtToken(BaseModel):
    access_token: str
    