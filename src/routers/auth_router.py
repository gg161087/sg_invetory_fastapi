from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from src.core.dependency import db_dependency
from src.schemas.user_schema import UserResponse
from src.schemas.auth_schema import Token
from src.core.security import authenticate_user, create_access_token, get_current_user, check_user
from src.core.config import ACCESS_TOKEN_EXPIRE_HOURS

router = APIRouter(
    prefix='/auth',
    tags=['Login']
)

@router.post('/token', summary='GET Access Token', response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No se pudo validar el usuario.')
    token = create_access_token(user.username, user.id, user.role, timedelta(ACCESS_TOKEN_EXPIRE_HOURS))
    return {'access_token': token, 'token_type': 'bearer'}

@router.get('/current_user', summary='GET current User', response_model=UserResponse)
def current_user(user:Annotated[dict, Depends(get_current_user)]):
    check_user(user)
    return user