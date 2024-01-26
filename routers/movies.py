from typing import List, Union, Dict, Any, Annotated
from annotated_types import Gt, Ge

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
    return Movie.init_movies(title, count, db)


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=schemas.Movie)
def add_movie_by_title(title: str, db: Session = Depends(database.get_db)):
    return Movie.add_movie_by_title(title, db)


@router.get("/list", status_code=status.HTTP_200_OK, response_model=schemas.MovieListPaginated)
def get_list_of_movies(limit: Annotated[int, Ge(0)] = 10, offset: Annotated[int, Ge(0)] = 0, db: Session = Depends(database.get_db)):
    total_records = Movie.get_record_count(db)
    movies = Movie.get_list_of_movies(limit, offset, db)
    return {
        "results": movies,
        "pagination": {
            "total_records": total_records,
            "count": len(movies),
            "limit": limit,
            "offset": offset
        }
    }


@router.get("/get", status_code=status.HTTP_200_OK, response_model=schemas.Movie)
def get_a_movie(imdb_id: str | None = None, title: str | None = None, db: Session = Depends(database.get_db)):
    return Movie.get_a_movie(imdb_id, title, db)


@router.delete("/delete/{imdb_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie_by_imdb_id(imdb_id: str, db: Session = Depends(database.get_db), currentUser: schemas.User = Depends(User.get_current_user)):
    return Movie.delete_movie_by_imdb_id(imdb_id, db, currentUser)
