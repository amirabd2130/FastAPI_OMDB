
from pydantic import BaseModel

from include.schemas import ListPagination


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


class MovieListPaginated(BaseModel):
    results: list[Movie] = []
    pagination: ListPagination
