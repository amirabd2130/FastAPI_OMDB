from fastapi import FastAPI
from include.models import create_models
from routers import authentication, movies, users

DESCRIPTION = """
A simple API service implemented using FastAPI to retrieve movie data from the OMDB API and store it in the database. The available endpoints are:

- `/user/create`: Used for creating a user. Requires specifying at least `username` and `password`.

- `/movie/init`: Fetches data from OMDB and stores it in the database if it's empty. You can specify a keyword like 'love' for `title` and use `count` to determine the number of records to retrieve.

- `/movie/add`: Searches for a movie by its `title` on OMDB, retrieves all details, and stores it in the database.

- `/movie/list`: Lists existing movies in the database. Optional parameters include `limit` (default 10) to specify the maximum records to return and `offset` (default 0) to specify the starting point. Records are sorted in ascending order by their `title`.

- `/movie/get`: Retrieves an existing movie from the database by its `imdb_id`, `title`, or both.

- `/movie/delete/{imdb_id}` [AUTHORIZATION REQUIRED]: Deletes an existing movie from the database by its `imdb_id`.

- `/movie/cleanup` [AUTHORIZATION REQUIRED]: Deletes all movies from the database.

NOTE: `/movie/init` and `/movie/cleanup` are included to facilitate testing.
"""

app = FastAPI(
    title="FastAPI - OMDB API",
    description=DESCRIPTION,
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
create_models()
