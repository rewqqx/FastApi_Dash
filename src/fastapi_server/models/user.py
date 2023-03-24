from sqlalchemy import Column, Integer, String, DateTime, Enum
from src.fastapi_server.models.base import Base
from sqlalchemy.sql import func
import enum


class RoleEnum(enum.Enum):
    admin = 1
    viewer = 2


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hashed = Column(String)
    role = Column(Enum(RoleEnum))
    created_at = Column(DateTime, server_default=func.now())

