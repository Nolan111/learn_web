from db import db_session
from models import Film
from youtub import get_video_id


films = db_session.query(Film).filter(Film.youtube_trailer_id == None).all()
for film in films:
    film.youtube_trailer_id = get_video_id(film.name)

    db_session.add(film)
    db_session.commit()
