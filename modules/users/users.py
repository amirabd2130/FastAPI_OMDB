import uuid

from fastapi import Depends
from include import database, exceptions, hashing, models, schemas
from modules.authentication.authentication import oauth2_scheme
from modules.authentication.token import JWTAuth
from sqlalchemy.orm import Session


class User():
    def create_user(request: schemas.User, db: Session):
        if not request.username or not request.password:
            raise exceptions.BAD_REQUEST_EXCEPTION
        else:
            user = db.query(models.User).where(
                models.User.username == request.username).first()
            if user:
                raise exceptions.USER_EXISTS_EXCEPTION
            else:
                newUser = models.User(
                    id=str(uuid.uuid4()),
                    first_name=request.first_name,
                    last_name=request.last_name,
                    username=request.username,
                    password=hashing.Hashing.Hash(request.password),)
                db.add(newUser)
                db.commit()
                db.refresh(newUser)
                return newUser

    def get_user_by_id(id: str, db: Session):
        user = db.query(models.User).where(models.User.id == id).first()
        if not user:
            raise exceptions.NOT_FOUND_EXCEPTION
        else:
            return user

    def get_user_by_username(username: str, db: Session):
        user = db.query(models.User).where(
            models.User.username == username).first()
        if user:
            return user

    def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
        token_data = JWTAuth.verify_token(token)
        user = User.get_user_by_username(token_data.username, db)
        if not user:
            raise exceptions.CREDENTIALS_EXCEPTION
        return user
