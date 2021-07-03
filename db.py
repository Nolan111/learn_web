from typing import Text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os

# with open("secret.txt", "r") as file:
#     pg_dsn = file.readline()
POSTGRES_DSN = os.getenv(
    "POSTGRES_DSN", "postgresql://rhfcsbxe:kVkKeqAlUrHYUZCiYa6P5AUdIiFtW6Ca@hattie.db.elephantsql.com/rhfcsbxe"
)
# print(POSTGRES_DSN)
engine = create_engine(POSTGRES_DSN)
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
