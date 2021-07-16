from typing import Text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os


POSTGRES_DSN = os.getenv(
    "POSTGRES_DSN", "postgresql://rhfcsbxe:kVkKeqAlUrHYUZCiYa6P5AUdIiFtW6Ca@hattie.db.elephantsql.com/rhfcsbxe"
)
engine = create_engine(POSTGRES_DSN)
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
