from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import List
from .files import File

import os

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 30
SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b"

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

router = APIRouter()


class User(BaseModel):
    username: str
    full_name: str
    email: str
    files: List[File]
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mourede.com",
        "files": [],
        "disabled": False,
        "password": "$2a$12$B2Gq.Dps1WYf2t57eiIKjO4DXC3IUMUXISJF62bSRiFfqMdOI2Xa6",
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mourede.com",
        "files": [],
        "disabled": True,
        "password": "$2a$12$SduE7dE.i3/ygwd0Kol8bOFvEABaoOOlC8JsCSr6wpwB4zl5STU4S",
    },
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception

    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo"
        )

    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto"
        )

    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña no es correcta",
        )

    access_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION),
    }

    return {
        "access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM),
        "token_type": "bearer",
    }


@router.get("/me")
async def me(user: User = Depends(current_user)):
    return user


""" @router.get("/")
async def read_users():
    return list_user """


""" @router.get("/{email}", tags=["users"])
async def user(email: str):
    return search_user(email) """


""" @router.post("/", response_model=User)
async def user(user: User):
    if type(search_user(user.email)) == User:
        raise HTTPException(
            status_code=409, detail="Ya existe un usuario registrado con ese email."
        )

    list_user.append(user)
    return user """


""" def search_user(email: str):
    user = filter(lambda user: user.email == email, list_user)
    try:
        return list(user)[0]
    except:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe ningún usuario registrado con el email: " + email,
        )
 """