# FastAPI_OMDB v1.0.0

A simple API service implemented using FastAPI to retrieve movie data from the OMDB API and store it in the local database. The endpoints include:

- `/user/create` to create a user.
- `/movie/init` to fetch data from OMDB and store it in the local database if the latter is empty.
- `/movie/add` to search for a movie by title, retrieve all details from OMDB, and store it in the local database.
- `/movie/list` to list existing movies in the local database. Optional parameters limit (default 10) and offset (default 0) can be set.
- `/movie/get` to retrieve a movie from the local database by imdb_id, title, or both.
- `/movie/delete/{imdb_id}` to delete a movie from the local database by imdb_id. Note: Authorization is required for this operation.

## Running outside docker

The Following environment variables must be set if you want to run the API outside docker:

```
export FASTAPI_OMDB_DATABASE_URL=sqlite:///fastapi_omdb_api
export FASTAPI_OMDB_OMDB_API_URL=https://www.omdbapi.com/
export FASTAPI_OMDB_OMDB_API_KEY=9ff9b2d1
export FASTAPI_OMDB_HASHING_SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
export FASTAPI_OMDB_HASHING_ALGORITHM=HS256
export FASTAPI_OMDB_ACCESS_TOKEN_EXPIRATION_MINUTES=30
```

Navigate to `FastAPI_OMDB` directory and run the following command:

`uvicorn main:app`

## Running using docker compose

Navigate to `FastAPI_OMDB` directory and run the following command:

`docker compose up --build`

## accessing the API service

Regardless of how you run the service, you can access the service in http://127.0.0.1:8000/docs this is the
