# FastAPI_OMDB v1.0.0

A simple API service implemented using FastAPI to retrieve movie data from the OMDB API and store it in the database. The available endpoints are:

- `/user/create`: Used for creating a user. Requires specifying at least `username` and `password`.

- `/movie/init`: Fetches data from OMDB and stores it in the database if it's empty. You can specify a keyword like 'love' for `title` and use `count` to determine the number of records to retrieve.

- `/movie/add`: Searches for a movie by its `title` on OMDB, retrieves all details, and stores it in the database.

- `/movie/list`: Lists existing movies in the database. Optional parameters include `limit` (default 10) to specify the maximum records to return and `offset` (default 0) to specify the starting point. Records are sorted in ascending order by their `title`.

- `/movie/get`: Retrieves an existing movie from the database by its `imdb_id`, `title`, or both.

- `/movie/delete/{imdb_id}` [AUTHORIZATION REQUIRED]: Deletes an existing movie from the database by its `imdb_id`.

- `/movie/cleanup` [AUTHORIZATION REQUIRED]: Deletes all movies from the database.

NOTE: `/movie/init` and `/movie/cleanup` are included to facilitate testing.

# GCP

# Requirement for this to work

- In your Cloud SQL, in Networking enable Private IP access
  `https://console.cloud.google.com/sql/instances/fastapi-omdb/connections/networking?project=personal-1-2130`
- In VPC Networks create a VPC Network (if not already created):
  `https://console.cloud.google.com/networking/networks/list?project=personal-1-2130`
- In Serverless VPC Access create a Connector:
  `https://console.cloud.google.com/networking/connectors/list?project=personal-1-2130`
- In Cloud SQL create a Connectivity Test, to test connection between different services and database:
  `https://console.cloud.google.com/sql/instances/fastapi-omdb/connections/tests?project=personal-1-2130`

## Deploy to GCP

Use `app.yaml` for deploying the service to GCP. IMPORTANT: Ensure to modify the env_variables in the file according to your project specifications and credentials.

Use the following command to deploy to GCP. Replace `PROJECT_NAME` and `VERSION_NUMBER`.

`gcloud app deploy --project PROJECT_NAME --version VERSION_NUMBER`

## Swagger Documentation & Testing

You can test the service using the Swagger documentation accessible below.

`https://fastapi-omdb-dot-personal-1-2130.ew.r.appspot.com/docs`

# Running Locally

## Running Outside docker

The Following environment variables must be set if you want to execute the API outside docker. You should update these with your credentials.

```sh
export FASTAPI_OMDB_DATABASE_URL=sqlite:///fastapi_omdb_api.db
export FASTAPI_OMDB_OMDB_API_URL=https://www.omdbapi.com/
export FASTAPI_OMDB_OMDB_API_KEY=9ff9b2d1
export FASTAPI_OMDB_HASHING_SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
export FASTAPI_OMDB_HASHING_ALGORITHM=HS256
export FASTAPI_OMDB_ACCESS_TOKEN_EXPIRATION_MINUTES=30
```

Navigate to `FastAPI_OMDB` directory and execute the following command:

`gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000`
OR
`uvicorn main:app --port 8000`

## Running Using `docker compose`

Navigate to `FastAPI_OMDB` directory and execute the following command:

`docker compose up --build`

## Swagger Documentation & Testing

You can test the service using the Swagger documentation accessible below.

`http://127.0.0.1:8000/docs`

# Tests

Navigate to `FastAPI_OMDB` directory and run the following command to execute all the tests:

`python3 -m pytest`
