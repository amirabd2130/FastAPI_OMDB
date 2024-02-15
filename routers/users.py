from fastapi import APIRouter, Depends, status
from include import database, schemas
from modules.users.users import User
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    return User().create_user(request, db)
