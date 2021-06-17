from bs4.element import ResultSet
from flask import Flask, render_template
from flask import request
from flask import json
from db import db_session
from models import Film
from bs4 import BeautifulSoup
import codecs
from flask import jsonify
import random


def create_app():
    app = Flask(__name__)

    films = [p for p in db_session.query(Film).all()]

    @app.route("/")
    def index():
        my_best__film = random.choice(films)
        result = {
            "name": my_best__film.name,
            "original_name": my_best__film.original_name,
            "country": my_best__film.country,
            "years": my_best__film.years,
            "genres": my_best__film.genres,
            "score_kinopoisk": my_best__film.score_kinopoisk,
        }
        return render_template(
            "index.html",
            name=my_best__film.name,
            original_name=my_best__film.original_name,
            country=my_best__film.country,
            years=my_best__film.years,
            genres=", ".join(my_best__film.genres),
            score_kinopoisk=my_best__film.score_kinopoisk,
            image="https://i.ytimg.com/vi/Wp3azsy_5Co/mqdefault.jpg",
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
