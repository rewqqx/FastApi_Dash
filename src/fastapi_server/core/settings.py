from pydantic import BaseSettings
import os
from dotenv import load_dotenv
from pathlib import Path


class Settings(BaseSettings):
    host: str
    port: int
    connection_string: str
    jwt_secret: str
    jwt_algorithm: str
    jwt_expires_seconds: int


settings = Settings(
    _env_file='../../.env',
    _env_file_encoding='utf-8',
)

dotenv_path = os.path.join(Path(os.getcwd()).parent, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)





