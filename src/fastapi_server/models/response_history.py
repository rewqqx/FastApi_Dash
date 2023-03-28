from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from src.fastapi_server.models.base import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum


class RequestEnum(enum.Enum):
    preprocessing = 1
    fit = 2
    predict = 3
    download = 4


class ResponseHistory(Base):
    __tablename__ = 'responses_history'
    id = Column(Integer, primary_key=True)
    request = Column(Enum(RequestEnum))
    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(Integer, ForeignKey('users.id'))

    user_created_by = relationship('User', foreign_keys=[created_by])
