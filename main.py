from fastapi import FastAPI
from include import database, models
from routers import authentication, movies, users

description = """
A simple API service implemented using FastAPI to retrieve movie data from the OMDB API and store it in the local database.

The endpoints include:
- `/user/create` to create a user.
- `/movie/init` to fetch data from OMDB and store it in the local database if the latter is empty.
- `/movie/add` to search for a movie by title, retrieve all details from OMDB, and store it in the local database.
- `/movie/list` to list existing movies in the local database. Optional parameters limit (default 10) and offset (default 0) can be set.
- `/movie/get` to retrieve a movie from the local database by imdb_id, title, or both.
- `/movie/delete/{imdb_id}` to delete a movie from the local database by imdb_id. Note: Authorization is required for this operation.
"""

app = FastAPI(
    title="OMDB API",
    description=description,
    version="1.0.0",
    contact={
        "name": "Amir Abdollahi",
        "url": "https://github.com/amirabd2130/FastAPI_OMDB",
        "email": "amirabd2130@yahoo.com",
    },
    openapi_tags=[
        {
            "name": "User",
            "description": "",
        },
        {
            "name": "Movie",
            "description": "",
        },
    ],
)
app.include_router(movies.router)
app.include_router(users.router)
app.include_router(authentication.router)

# create tables if they don't exist in the database
models.Base.metadata.create_all(bind=database.engine)
