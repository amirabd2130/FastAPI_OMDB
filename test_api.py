from fastapi.testclient import TestClient
from include import models
from include.database import get_db
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///fastapi_omdb_api_test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_start():
    # create all the tables from test db
    models.Base.metadata.create_all(bind=engine)


def test_movie_list__empty_db():
    response = client.get("/movie/list")
    assert response.status_code == 200
    response = response.json()
    assert len(response["results"]) == 0
    assert response["pagination"]["total_records"] == 0
    assert response["pagination"]["count"] == 0
    assert response["pagination"]["limit"] == 10
    assert response["pagination"]["offset"] == 0


def test_movie_init__missing_param():
    response = client.get("/movie/init")
    assert response.status_code == 422


def test_movie_init__empty_db():
    response = client.get("/movie/init?title=you&count=10")
    assert response.status_code == 201
    response = response.json()
    assert response == "10 movies has been added to the database"


def test_movie_init__not_empty_db():
    response = client.get("/movie/init?title=you&count=10")
    assert response.status_code == 201
    response = response.json()
    assert response == "The movie table is not empty. Nothing new added to the database."


def test_movie_list():
    response = client.get("/movie/list?limit=5&offset=2")
    assert response.status_code == 200
    response = response.json()
    assert len(response["results"]) == 5
    assert response["pagination"]["total_records"] == 10
    assert response["pagination"]["count"] == 5
    assert response["pagination"]["limit"] == 5
    assert response["pagination"]["offset"] == 2


def test_movie_list__out_of_bound():
    response = client.get("/movie/list?limit=5&offset=20")
    assert response.status_code == 200
    response = response.json()
    assert len(response["results"]) == 0
    assert response["pagination"]["total_records"] == 10
    assert response["pagination"]["count"] == 0
    assert response["pagination"]["limit"] == 5
    assert response["pagination"]["offset"] == 20


def test_movie_list__negative_params():
    response = client.get("/movie/list?limit=-5&offset=-20")
    assert response.status_code == 422


def test_movie_add__missing_param():
    response = client.post("/movie/add")
    assert response.status_code == 400


def test_movie_add():
    response = client.post("/movie/add?title=Iron Man")
    assert response.status_code == 201
    response = response.json()
    assert response["imdb_id"] == "tt0371746"


def test_movie_add__duplicate():
    response = client.post("/movie/add?title=Iron Man")
    assert response.status_code == 409


def test_movie_add__non_existing_movie():
    response = client.post("/movie/add?title=ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    assert response.status_code == 404


def test_movie_get__missing_param():
    response = client.get("/movie/get")
    assert response.status_code == 400


def test_movie_get__with_id_existing_movie():
    response = client.get("/movie/get?imdb_id=tt0371746")
    assert response.status_code == 200
    response = response.json()
    assert response["imdb_id"] == "tt0371746"
    assert response["title"] == "Iron Man"


def test_movie_get__with_id_non_existing_movie():
    response = client.get("/movie/get?imdb_id=1234567890")
    assert response.status_code == 404


def test_movie_get__with_title_existing_movie():
    response = client.get("/movie/get?title=Iron Man")
    assert response.status_code == 200
    response = response.json()
    assert response["imdb_id"] == "tt0371746"
    assert response["title"] == "Iron Man"


def test_movie_get__with_title_non_existing_movie():
    response = client.get("/movie/get?title=ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    assert response.status_code == 404


def test_movie_get__with_both_params_matching():
    response = client.get("/movie/get?imdb_id=tt0371746&title=Iron Man")
    assert response.status_code == 200
    response = response.json()
    assert response["imdb_id"] == "tt0371746"
    assert response["title"] == "Iron Man"


def test_movie_get__with_both_params_mismatching():
    response = client.get("/movie/get?imdb_id=1234567890&title=Iron Man")
    assert response.status_code == 404


def test_user_create__missing_param():
    response = client.post("/user", json={"first_name": "first 1", "last_name": "last 1",
                           "username": "user"})
    assert response.status_code == 422


def test_user_create():
    response = client.post("/user", json={"first_name": "first 1", "last_name": "last 1",
                           "username": "user", "password": "password"})
    assert response.status_code == 201


def test_user_create__duplicate():
    response = client.post("/user", json={"first_name": "first 2", "last_name": "last 2",
                           "username": "user", "password": "password"})
    assert response.status_code == 409


def test_login():
    response = client.post("/login",
                           data={"username": "user", "password": "password"})
    assert response.status_code == 201


def test_login__incorrect_credentials():
    response = client.post("/login",
                           data={"username": "user", "password": "wrong"})
    assert response.status_code == 401


def test_movie_delete__unauthorized():
    response = client.delete("/movie/delete/ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                             headers={"Authorization": 'Bearer ABCD'})
    assert response.status_code == 401


def test_movie_delete__non_existing_movie():
    response = client.post("/login",
                           data={"username": "user", "password": "password"})
    assert response.status_code == 201
    response = response.json()

    response = client.delete("/movie/delete/ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                             headers={"Authorization": f'Bearer {response["access_token"]}'})
    assert response.status_code == 404


def test_movie_delete():
    response = client.post("/login",
                           data={"username": "user", "password": "password"})
    assert response.status_code == 201
    response = response.json()

    response = client.delete("/movie/delete/tt0371746",
                             headers={"Authorization": f'Bearer {response["access_token"]}'})
    assert response.status_code == 204


def test_finish():
    # delete all the tables from test db
    models.Base.metadata.drop_all(bind=engine)
