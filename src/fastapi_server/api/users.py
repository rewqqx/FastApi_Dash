from fastapi.security import OAuth2PasswordRequestForm

from src.fastapi_server.models.schemas.utils.jwt_token import JwtToken

from fastapi import APIRouter, Depends, HTTPException, status
from src.fastapi_server.models.schemas.user.user_request import UserRequest
from src.fastapi_server.models.schemas.user.user_response import UserResponse
from src.fastapi_server.services.users import UsersService
from src.fastapi_server.services.users import get_current_user_id, check_admin

router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.post('/authorize', response_model=JwtToken, name='Авторизация')
def authorize(auth_schema: OAuth2PasswordRequestForm = Depends(), users_service: UsersService = Depends()):
    """
    Авторизация
    """
    result = users_service.authorize(auth_schema.username, auth_schema.password)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не авторизован')
    return result


@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED, name="Добавить пользователя")
def add(user_schema: UserRequest, users_service: UsersService = Depends(), user_req: int = Depends(check_admin)):
    """
    Добавить пользователя
    """
    user = users_service.add(user_schema)
    user.role = user.role.name
    return user
