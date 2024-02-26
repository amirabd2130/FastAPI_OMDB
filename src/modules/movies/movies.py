import uuid

from sqlalchemy import func
from sqlalchemy.orm import Session

from include import exceptions, models, omdb, schemas


class Movie:

    def get_record_count(self, db: Session):
        return db.query(models.Movie).count()

    def create_movie_object(self, movie_data):
        imdb_votes, imdb_rating, metascore, box_office, ratings = 0, 0, 0, 0, {}
        if movie_data.get("imdbVotes") != "N/A":
            imdb_votes = int(movie_data.get("imdbVotes").replace(",", ""))
        if movie_data.get("imdbRating") != "N/A":
            imdb_rating = movie_data.get("imdbRating")
        if movie_data.get("Metascore") != "N/A":
            metascore = movie_data.get("Metascore")
        if movie_data.get("BoxOffice") != "N/A":
            box_office = float(movie_data.get("BoxOffice").replace(",", "").replace("$", ""))
        if movie_data.get("Ratings") != "N/A":
            for item in movie_data.get("Ratings"):
                ratings[item["Source"]] = item["Value"]

        return models.Movie(
            id=str(uuid.uuid4()),
            imdb_id=movie_data.get("imdbID"),
            title=movie_data.get("Title"),
            year=movie_data.get("Year"),
            type=movie_data.get("Type"),
            genre=movie_data.get("Genre"),
            director=movie_data.get("Director"),
            writer=movie_data.get("Writer"),
            actors=movie_data.get("Actors"),
            imdb_votes=imdb_votes,
            imdb_rating=imdb_rating,
            plot=movie_data.get("Plot"),
            rated=movie_data.get("Rated"),
            released=movie_data.get("Released"),
            runtime=movie_data.get("Runtime"),
            language=movie_data.get("Language"),
            country=movie_data.get("Country"),
            awards=movie_data.get("Awards"),
            poster=movie_data.get("Poster"),
            ratings=ratings,
            metascore=metascore,
            dvd=movie_data.get("DVD"),
            box_office=box_office,
            production=movie_data.get("Production"),
            website=movie_data.get("Website"),
        )

    def init(self, title: str, count: int, db: Session):
        if not title or not count:
            raise exceptions.BAD_REQUEST_EXCEPTION
        if self.get_record_count(db) > 0:
            return "The movie table is not empty. Nothing new added to the database."

        movie_count, page = 0, 2
        while movie_count < count:
            movies_data = omdb.get_movie_detail_by_title(title, page)
            if not movies_data:
                raise exceptions.OMDB_API_ERROR
            for movie_data in movies_data:
                if movie_count == count:
                    break
                movie_count += 1
                movie_data_details = omdb.get_movie_detail_by_id(movie_data.get("imdbID"))
                if not movie_data_details:
                    raise exceptions.OMDB_API_ERROR
                new_movie = self.create_movie_object(movie_data_details)
                db.add(new_movie)
            page += 1
        db.commit()
        return f"{movie_count} movies has been added to the database"

    def add_by_title(self, title: str, db: Session):
        if not title:
            raise exceptions.BAD_REQUEST_EXCEPTION
        movie_data = omdb.get_movie_detail_by_title(title, 1, "t")
        if not movie_data:
            raise exceptions.OMDB_API_ERROR
        # check if movie already exists in the db
        movie_in_db = db.query(models.Movie).where(models.Movie.imdb_id == movie_data["imdbID"]).first()
        if movie_in_db:
            raise exceptions.MOVIE_EXISTS_EXCEPTION
        new_movie = self.create_movie_object(movie_data)
        db.add(new_movie)
        db.commit()
        return new_movie

    def get_one(self, imdb_id: str, title: str, db: Session):
        if not imdb_id and not title:
            raise exceptions.BAD_REQUEST_EXCEPTION
        elif imdb_id and title:
            movie = db.query(models.Movie).where(models.Movie.imdb_id == imdb_id).where(
                func.lower(models.Movie.title) == title.lower()).first()
        elif imdb_id:
            movie = db.query(models.Movie).where(models.Movie.imdb_id == imdb_id).first()
        elif title:
            movie = db.query(models.Movie).where(func.lower(models.Movie.title) == title.lower()).first()

        if not movie:
            raise exceptions.NOT_FOUND_EXCEPTION
        return movie

    def get_list(self, limit: int, offset: int, db: Session):
        total_records = self.get_record_count(db)
        movies = db.query(models.Movie).order_by(models.Movie.title.asc()).offset(offset).limit(limit).all()
        return schemas.MovieListPaginated(
            results=[schemas.Movie(**a.__dict__) for a in movies],
            pagination=schemas.ListPagination(total_records=total_records,
                                              count=len(movies),
                                              limit=limit,
                                              offset=offset))

    def delete_by_imdb_id(self, imdb_id: str, db: Session, current_user: schemas.User):
        movie = db.query(models.Movie).where(models.Movie.imdb_id == imdb_id)
        if not movie.first():
            raise exceptions.NOT_FOUND_EXCEPTION
        movie.delete()
        db.commit()

    def delete_all(self, db: Session, current_user: schemas.User):
        movie = db.query(models.Movie).where(True)
        if movie:
            movie.delete()
            db.commit()
