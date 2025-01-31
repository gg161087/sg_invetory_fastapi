from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.config.dependency import db_dependency
from app.auth.jwt_handler import authenticate_user, create_access_token, get_current_user, check_user
from app.config.settings import settings

def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No se pudo validar el usuario.')
    token = create_access_token(user.username, user.id, user.role, timedelta(settings.ACCESS_TOKEN_EXPIRE_HOURS))
    return {'access_token': token, 'token_type': 'bearer'}

def current_user(user:Annotated[dict, Depends(get_current_user)]):
    check_user(user)
    return user