import os
from datetime import datetime, timedelta, UTC
from typing import Union

from include import exceptions, schemas
from jose import JWTError, jwt

SECRET_KEY = os.environ.get("FASTAPI_OMDB_HASHING_SECRET_KEY")
ALGORITHM = os.environ.get("FASTAPI_OMDB_HASHING_ALGORITHM")
TOKEN_EXPIRATION = int(os.environ.get(
    "FASTAPI_OMDB_ACCESS_TOKEN_EXPIRATION_MINUTES"))


class JWTAuth():
    def create_token(self, data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=TOKEN_EXPIRATION)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise exceptions.CREDENTIALS_EXCEPTION
            return schemas.TokenData(username=username)
        except JWTError:
            raise exceptions.CREDENTIALS_EXCEPTION
