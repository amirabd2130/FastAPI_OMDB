from fastapi import HTTPException, status

# 400
BAD_REQUEST_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Cannot process the request, check your request",)

# 401
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},)

# 404
NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="The record with provided detail deos not exist")

# 404
OMDB_API_ERROR = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Could not fetch data from OMDB API")

# 409
MOVIE_EXISTS_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The movie already exists")

# 409
USER_EXISTS_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The username already exists")

# 500
INTERNAL_SERVER_ERROR = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal server error",)
