from sqlalchemy.orm import session
from models import Film
from db import db_session
import requests
from bs4 import BeautifulSoup
import json
import requests
import time
import os
from requests.api import patch


def save_film_db(film_data):
    try:
        film = Film(
            name=film_data["name"],
            original_name=film_data["original_name"],
            country=film_data["country"],
            years=film_data["years"],
            genres=film_data["genres"],
            score_kinopoisk=film_data["score_kinopoisk"],
            image=film_data["image"],
            id=film_data["id"],
        )

        db_session.add(film)
        db_session.commit()
    except (Exception) as e:
        db_session.rollback()
        print("Data base Error - film_id", film_data["id"])


def json_w(film_data, file_name):
    with open(f"films/films_{file_name}.json", "w", encoding="utf8") as f:
        json.dump(film_data, f, ensure_ascii=False, indent=4)


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


def get_file(picture):
    try:
        response = requests.get(picture, stream=True)
        response.raise_for_status()
        return response
    except:
        return


def dowload_image(url, name):
    response = get_file(url)
    if not response:
        return
    file = open(name, "bw")
    for chunk in response.iter_content(4096):
        file.write(chunk)
    return True


def get_python_hd(html, film_id):
    try:
        soup = BeautifulSoup(html, "html.parser")
        film = soup.find("div", class_="title")
        result = []

        name = film.find("h1").text
        original_name = film.find("h2").text

        class_film = soup.find("div", class_="navigation")
        country = class_film.find("a", class_="nav-button border-radius--4 categories", type="country").text
        year = class_film.find("a", class_="nav-button border-radius--4 categories", type="year").text
        genres = []
        for g in class_film.findAll("a", class_="nav-button border-radius--4 categories", type="genre"):
            genres.append(g.text)

        score_ = film.find("div", class_="margin-bottom--24").text.strip()

        image = soup.find("meta", property="og:image")["content"]
        image_url = f"https://randomfilms.ru{image}"
        image_name = f"films/image_{film_id}.jpeg"

        # if not dowload_image(url=image_url, name=image_name):
        #     image_name = None

        film_data = {
            "id": film_id,
            "name": name,
            "original_name": original_name,
            "country": country,
            "years": year,
            "genres": genres,
            "score_kinopoisk": score_,
            "image": image_name,
        }
        print(film_id)
        result.append(film_data)

        # json_w(result, file_name=str(film_id))
        save_film_db(film_data)

    except Exception as e:
        print(film_id, "Error", e)
    else:
        print(film_id, "OK")


if __name__ == "__main__":
    if not os.path.isdir("films"):
        os.mkdir("films")
    number = 30000
    for film_id in range(1, number + 1):

        url = f"https://randomfilms.ru/film/{film_id}"
        html = get_html(url)
        if html:
            get_python_hd(html, film_id)
