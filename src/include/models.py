from include import database
from modules.movies.models import *
from modules.users.models import *


def create_models():
    # table_objects = [database.Base.metadata.tables[Movie.__tablename__],
    #                  database.Base.metadata.tables[User.__tablename__]]
    # database.Base.metadata.create_all(bind=database.engine, tables=table_objects)

    database.Base.metadata.create_all(bind=database.engine)
