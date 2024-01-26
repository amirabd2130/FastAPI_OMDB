from include.database import Base
from modules.movies.models import *
from sqlalchemy import Column, String


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    status = Column(String(50))
