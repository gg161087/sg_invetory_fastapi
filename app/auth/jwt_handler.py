from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Annotated
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from app.config.settings import settings
from app.services.user_service import read_user_by_username
from app.schemas.auth_schema import TokenData

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return bcrypt_context.hash(password)

def authenticate_user(username: str, password: str, db):
    user = read_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def check_user(user):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Autenticación fallida.', headers={"WWW-Authenticate": "Bearer"})

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        check_user(username)
        token_data = TokenData(id=user_id, username=username, user_role=user_role)
        return token_data
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No se pudo validar el usuario.')
    
def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expire = datetime.utcnow() + expires_delta
    encode.update({'exp': expire})
    encoded_jwt = jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
