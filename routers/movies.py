from typing import Annotated

from annotated_types import Ge
from fastapi import APIRouter, Depends, status
from include import database, schemas
from modules.movies.movies import Movie
from modules.users.users import User
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/movie",
    tags=["Movie"],
)


@router.get("/init", status_code=status.HTTP_201_CREATED)
def init_movies(title: str, count: Annotated[int, Ge(0)], db: Session = Depends(database.get_db)):
    return Movie().init(title, count, db)


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=schemas.Movie)
def add_movie_by_title(title: str = "", db: Session = Depends(database.get_db)):
    return Movie().add_by_title(title, db)


@router.get("/list", status_code=status.HTTP_200_OK, response_model=schemas.MovieListPaginated)
def get_list_of_movies(limit: Annotated[int, Ge(0)] = 10, offset: Annotated[int, Ge(0)] = 0, db: Session = Depends(database.get_db)):
    return Movie().get_list(limit, offset, db)


@router.get("/get", status_code=status.HTTP_200_OK, response_model=schemas.Movie)
def get_a_movie(imdb_id: str | None = None, title: str | None = None, db: Session = Depends(database.get_db)):
    return Movie().get_one(imdb_id, title, db)


@router.delete("/delete/", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie_by_imdb_id(imdb_id: str, db: Session = Depends(database.get_db), currentUser: schemas.User = Depends(User().get_current_user)):
    return Movie().delete_by_imdb_id(imdb_id, db, currentUser)


@router.delete("/cleanup", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_movies(db: Session = Depends(database.get_db), currentUser: schemas.User = Depends(User().get_current_user)):
    return Movie().delete_all(db, currentUser)
