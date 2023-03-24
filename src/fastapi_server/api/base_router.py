from fastapi import APIRouter

from src.fastapi_server.api import users, models

router = APIRouter()
router.include_router(users.router)
router.include_router(models.router)


