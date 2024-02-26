from sqlalchemy import JSON, Column, Float, Integer, String, Text

from include.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(String(36), primary_key=True, index=True, nullable=False)
    imdb_id = Column(String(20), nullable=True)
    title = Column(String(255), nullable=True)
    year = Column(Integer, nullable=True)
    type = Column(String(20), nullable=True)
    genre = Column(String(255), nullable=True)
    director = Column(String(255), nullable=True)
    writer = Column(String(255), nullable=True)
    actors = Column(String(255), nullable=True)
    imdb_votes = Column(Integer, nullable=True)
    imdb_rating = Column(Float(2), nullable=True)
    plot = Column(Text, nullable=True)
    rated = Column(String(20), nullable=True)
    released = Column(String(25), nullable=True)
    runtime = Column(String(10), nullable=True)
    language = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)
    awards = Column(Text, nullable=True)
    poster = Column(String(255), nullable=True)
    ratings = Column(JSON, nullable=True)
    metascore = Column(Integer, nullable=True)
    dvd = Column(String(25), nullable=True)
    box_office = Column(Float(2), nullable=True)
    production = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
