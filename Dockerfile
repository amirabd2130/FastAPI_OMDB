FROM python:3.11

# ensure `.pyc` files will not be created
ENV PYTHONDONTWRITEBYTECODE 1
# this keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1
# ensure `pip` does not use a cache directory
ENV PIP_NO_CACHE_DIR 1

# database URL
ENV FASTAPI_OMDB_DATABASE_URL=sqlite:///fastapi_omdb_api.db
# OMDB API URL/KEY (email used: amirabd2130@yahoo.com)
ENV FASTAPI_OMDB_OMDB_API_URL=https://www.omdbapi.com/
ENV FASTAPI_OMDB_OMDB_API_KEY=9ff9b2d1
# hashing
ENV FASTAPI_OMDB_HASHING_SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ENV FASTAPI_OMDB_HASHING_ALGORITHM=HS256
ENV FASTAPI_OMDB_ACCESS_TOKEN_EXPIRATION_MINUTES=30

# create a non-root user `python:python`
RUN groupadd --gid 1000 python && useradd --uid 1000 --gid python --shell /bin/bash --create-home python

# create app directory using non-root user
RUN mkdir -p /home/python/app
WORKDIR /home/python/app

# copy files
COPY . .
RUN chown -R python:python /home/python/app

# update pip and install dependencies
# RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

USER 1000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
