from fastapi import FastAPI

from src.fastapi_server.api.base_router import router

app = FastAPI(
    title='Final Task',
    description='Api. Kirill Obukhov',
    version='0.9',
)

app.include_router(router)
