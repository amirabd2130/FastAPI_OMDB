# FastAPI_OMDB v1.0.0

A simple API service implemented using FastAPI to retrieve movie data from the OMDB API and store it in the database. The endpoints include:

- `/user/create` to create a user.

- `/movie/init` to fetch data from OMDB and store it in the database if the latter is empty.

- `/movie/add` to search for a movie by title, retrieve all details from OMDB, and store it in the database.

- `/movie/list` to list existing movies in the database. Optional parameters limit (default 10) and offset (default 0) can be set.

- `/movie/get` to retrieve a movie from the database by imdb_id, title, or both.

- `/movie/delete/{imdb_id}` to delete a movie from the database by imdb_id. Note: Authorization is required for this operation.

- `/movie/cleanup` to delete all the movies from the database

NOTE: `/movie/init` and `/movie/cleanup` are there to make the testing easier

# GCP

## Deploy to GCP

Using `app.yaml` will deploy to GCP and can be access here:

`gcloud app deploy --project personal-1-2130 --version 1`

## Access the Deployed Service

`https://fastapi-omdb-dot-personal-1-2130.ew.r.appspot.com/docs`

# Running Locally

## Running Outside docker

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

`gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000`

## Running Using `docker compose`

Navigate to `FastAPI_OMDB` directory and run the following command:

`docker compose up --build`

## Accessing the API Documentation and Testing

Regardless of how you run the service, you can access the swagger documentation at http://127.0.0.1:8000/docs

# Tests

Navigate to `FastAPI_OMDB` directory and run the following command:

`python3 -m pytest`
