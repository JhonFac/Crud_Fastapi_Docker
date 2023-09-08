from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import CreateUserRequest, Token

# Clave secreta utilizada para firmar tokens JWT.
SECRET_KEY = 'IMAGINETEST_!1"2#3$4'

# Algoritmo utilizado para firmar tokens JWT.
ALGORITHM = "HS256"

# Instancia de CryptContext para el manejo de contraseñas.
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer para la autenticación mediante token.
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

# Anotación para la dependencia que obtiene la sesión de la base de datos.
db_dependency = Annotated[Session, Depends(get_db)]


# Función para validar la existencia de un usuario autenticado.
def validate_user(user: str):
    if user is None:
        raise HTTPException(status_code=401, detail="Autenticación fallida")


# Función para autenticar a un usuario.
def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


# Función para crear un token de acceso JWT.
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# Función para obtener el usuario actual a partir del token JWT.
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No se pudo validar al usuario.")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No se pudo validar al usuario.")
