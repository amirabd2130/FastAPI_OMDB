from typing import List

from include.schemas import ListPagination
from pydantic import BaseModel


class Movie(BaseModel):
    imdb_id: str
    title: str
    year: int
    type: str
    genre: str
    director: str
    writer: str
    actors: str
    imdb_votes: int
    imdb_rating: float
    plot: str
    rated: str
    released: str
    runtime: str
    language: str
    country: str
    awards: str
    poster: str
    ratings: dict
    metascore: int
    dvd: str
    box_office: float
    production: str
    website: str

    class Config():
        orm_mode = True


class MovieListPaginated(BaseModel):
    results: List[Movie] = []
    pagination: ListPagination
