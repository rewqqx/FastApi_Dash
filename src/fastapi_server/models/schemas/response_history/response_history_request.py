from pydantic import BaseModel


class ResponseHistoryRequest(BaseModel):
    request: int
