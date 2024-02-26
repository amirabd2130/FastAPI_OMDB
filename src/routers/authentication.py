from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from include import database
from modules.authentication.authentication import Authentication


router = APIRouter(
    prefix="/login",
    tags=["User"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    return Authentication().login(data, db)
