from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.config.dependency import db_dependency
from app.schemas.user_schema import UserResponse
from app.schemas.auth_schema import Token
from app.auth.jwt_handler import get_current_user
from app.controllers import auth_controller

router = APIRouter(prefix='/auth', tags=['Login'])

@router.post('/token', summary='GET Access Token', response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    return auth_controller.login_for_access_token(form_data, db)

@router.get('/current_user', summary='GET current User', response_model=UserResponse)
def current_user(user:Annotated[dict, Depends(get_current_user)]):
    return auth_controller.current_user(user)