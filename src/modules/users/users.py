import uuid

from fastapi import Depends
from sqlalchemy.orm import Session

from include import database, exceptions, models, schemas
from include.hashing import Hashing
from modules.authentication.authentication import oauth2_scheme
from modules.authentication.token import JWTAuth


class User:
    def create_user(self, request: schemas.User, db: Session):
        if not request.username or not request.password:
            raise exceptions.BAD_REQUEST_EXCEPTION
        user = db.query(models.User).where(
            models.User.username == request.username).first()
        if user:
            raise exceptions.USER_EXISTS_EXCEPTION
        new_user = models.User(
            id=str(uuid.uuid4()),
            first_name=request.first_name,
            last_name=request.last_name,
            username=request.username,
            password=Hashing().hash(request.password),)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def get_user_by_username(self, username: str, db: Session):
        user = db.query(models.User).where(models.User.username == username).first()
        if not user:
            return None
        return user

    def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
        token_data = JWTAuth().verify_token(token)
        user = self.get_user_by_username(token_data.username, db)
        if not user:
            raise exceptions.CREDENTIALS_EXCEPTION
        return user
