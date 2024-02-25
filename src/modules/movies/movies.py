import uuid

from include import exceptions, models, omdb, schemas
from sqlalchemy import func
from sqlalchemy.orm import Session


class Movie:

    def get_record_count(self, db: Session):
        return db.query(models.Movie).count()

    def create_movie_object(self, movieData):
        imdbVotes, imdbRating, metascore, boxOffice, ratings = 0, 0, 0, 0, {}
        if movieData.get("imdbVotes") != "N/A":
            imdbVotes = int(movieData.get("imdbVotes").replace(",", ""))
        if movieData.get("imdbRating") != "N/A":
            imdbRating = movieData.get("imdbRating")
        if movieData.get("Metascore") != "N/A":
            metascore = movieData.get("Metascore")
        if movieData.get("BoxOffice") != "N/A":
            boxOffice = float(movieData.get("BoxOffice").replace(",", "").replace("$", ""))
        if movieData.get("Ratings") != "N/A":
            for item in movieData.get("Ratings"):
                ratings[item["Source"]] = item["Value"]

        return models.Movie(
            id=str(uuid.uuid4()),
            imdb_id=movieData.get("imdbID"),
            title=movieData.get("Title"),
            year=movieData.get("Year"),
            type=movieData.get("Type"),
            genre=movieData.get("Genre"),
            director=movieData.get("Director"),
            writer=movieData.get("Writer"),
            actors=movieData.get("Actors"),
            imdb_votes=imdbVotes,
            imdb_rating=imdbRating,
            plot=movieData.get("Plot"),
            rated=movieData.get("Rated"),
            released=movieData.get("Released"),
            runtime=movieData.get("Runtime"),
            language=movieData.get("Language"),
            country=movieData.get("Country"),
            awards=movieData.get("Awards"),
            poster=movieData.get("Poster"),
            ratings=ratings,
            metascore=metascore,
            dvd=movieData.get("DVD"),
            box_office=boxOffice,
            production=movieData.get("Production"),
            website=movieData.get("Website"),
        )

    def init(self, title: str, count: int, db: Session):
        if not title or not count:
            raise exceptions.BAD_REQUEST_EXCEPTION
        if self.get_record_count(db) > 0:
            return "The movie table is not empty. Nothing new added to the database."

        movieCount, page = 0, 2
        while movieCount < count:
            moviesData = omdb.get_movie_detail_by_title(title, page)
            if not moviesData:
                raise exceptions.OMDB_API_ERROR
            for movieData in moviesData:
                if movieCount == count:
                    break
                movieCount += 1
                movieDataDetails = omdb.get_movie_detail_by_id(movieData.get("imdbID"))
                if not movieDataDetails:
                    raise exceptions.OMDB_API_ERROR
                newMovie = self.create_movie_object(movieDataDetails)
                db.add(newMovie)
            page += 1
        db.commit()
        return f"{movieCount} movies has been added to the database"

    def add_by_title(self, title: str, db: Session):
        if not title:
            raise exceptions.BAD_REQUEST_EXCEPTION
        movieData = omdb.get_movie_detail_by_title(title, 1, "t")
        if not movieData:
            raise exceptions.OMDB_API_ERROR
        # check if movie already exists in the db
        movieInDb = db.query(models.Movie).where(models.Movie.imdb_id == movieData["imdbID"]).first()
        if movieInDb:
            raise exceptions.MOVIE_EXISTS_EXCEPTION
        newMovie = self.create_movie_object(movieData)
        db.add(newMovie)
        db.commit()
        return newMovie

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

    def delete_by_imdb_id(self, imdb_id: str, db: Session, currentUser: schemas.User):
        movie = db.query(models.Movie).where(models.Movie.imdb_id == imdb_id)
        if not movie.first():
            raise exceptions.NOT_FOUND_EXCEPTION
        movie.delete()
        db.commit()

    def delete_all(self, db: Session, currentUser: schemas.User):
        movie = db.query(models.Movie).where(True)
        if movie:
            movie.delete()
            db.commit()
