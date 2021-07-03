from flask import Flask, render_template
from flask import request
from db import db_session
from models import Film

import random
from filter import countries_filter, genres_filter

genres_list = list(genres_filter)
genres_list.sort()
countries_list = list(countries_filter)
countries_list.sort()


def cast_into_int(number):
    try:
        number = int(number)
    except:
        number = 0
    return number


def films_filter(genere, country, to, from_):
    filter_film = db_session.query(Film)
    if cast_into_int(to) in range(1915, 2018):
        filter_film = filter_film.filter(Film.years <= to)
    if cast_into_int(from_) in range(1915, 2018):
        filter_film = filter_film.filter(Film.years >= from_)
    if country in countries_filter:
        filter_film = filter_film.filter(Film.country == country)
    if genere in genres_filter:
        filter_film = filter_film.filter(Film.genres.comparator.any(genere))

    result = filter_film.all()
    if not result:
        result = db_session.query(Film).all()
    return result


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        from_ = request.args.get("from", "1915")
        to = request.args.get("to", "2018")
        country = request.args.get("country", "Любая")
        genere = request.args.get("genere", "Любой")
        films = films_filter(from_=from_, to=to, country=country, genere=genere)
        my_best__film = random.choice(films)

        return render_template(
            "index.html",
            countries_list=countries_list,
            genres_list=genres_list,
            search_genere=genere,
            search_country=country,
            search_from_=from_,
            search_to=to,
            name=my_best__film.name,
            original_name=my_best__film.original_name,
            country=my_best__film.country,
            years=my_best__film.years,
            genres=", ".join(my_best__film.genres),
            score_kinopoisk=my_best__film.score_kinopoisk,
            image="https://upload.wikimedia.org/wikipedia/ru/6/61/Lock_Stock_and_Two_Smoking_Barrels_Poster.jpg",
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, threaded=False)
