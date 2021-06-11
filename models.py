from sqlalchemy import Column, Integer, String, ARRAY

from db import Base, engine


class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True)
    name = Column(String())
    original_name = Column(String())
    country = Column(String())
    years = Column(Integer())
    genres = Column(ARRAY(String))
    score_kinopoisk = Column(String(25))
    image = Column(String(25))

    def __repr__(self):
        return f"Film {self.id}, {self.name}"


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
