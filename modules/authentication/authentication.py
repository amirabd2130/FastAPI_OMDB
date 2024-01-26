from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from include import exceptions, hashing, models
from modules.authentication.token import JWTAuth
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class Authentication():
    def login(request: OAuth2PasswordRequestForm, db: Session):
        user = db.query(models.User).where(
            models.User.username == request.username).first()
        if not user:
            raise exceptions.CREDENTIALS_EXCEPTION
        else:
            if not hashing.Hashing.Verify(request.password, user.password):
                raise exceptions.CREDENTIALS_EXCEPTION
            else:
                access_token = JWTAuth.create_token(
                    data={"sub": user.username})
                return {"access_token": access_token, "token_type": "bearer"}
