import requests
from bs4 import BeautifulSoup
import json
import requests
import time
import random
from fp import FreeProxy


def csv_w(film_data, file_name):
    with open(f"python-org-kinopoisk_{file_name}.json", "w", encoding="utf8") as f:
        json.dump(film_data, f, ensure_ascii=False, indent=4)


s = requests.session()


def get_html(url, params=None):

    try:
        result = s.get(
            url,
            params=params,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
            },
        )
        result.raise_for_status()

        return result.text
    except (requests.RequestException, ValueError):
        print("Сетевая ошибка")
    return False


def get_pages_count(html):
    soup = BeautifulSoup(html, "html.parser")
    pagination = soup.findAll("a", class_="paginator__page-number")
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_python_kinopoisk(html, page_number):
    soup = BeautifulSoup(html, "html.parser")
    film_list = soup.findAll("div", class_="desktop-seo-selection-film-item selection-list__film")
    result = []

    for film in film_list:
        name = film.find("p", class_="selection-film-item-meta__name").text
        original_name = film.find("p", class_="selection-film-item-meta__original-name").text
        on_date = original_name.split(", ")
        original_name = on_date[0]
        date = on_date[-1]
        meta = film.find("p", class_="selection-film-item-meta__meta-additional")
        country, tags = meta.findAll("span", class_="selection-film-item-meta__meta-additional-item")
        country = country.text
        tags = tags.text.split(", ")
        id = film.find("a", class_="selection-film-item-meta__link")["href"][6:-1]

        film_data = {
            "name": name,
            "original_name": original_name,
            "country": country,
            "tags": tags,
            "id": int(id),
            "date": date,
        }
        result.append(film_data)
        print(name, original_name, country, tags)

    csv_w(result, file_name=str(page_number))


if __name__ == "__main__":
    url = "https://www.kinopoisk.ru/lists/navigator/?tab=all"
    html = get_html(url)
    print(len(html))
    if html:
        movie = []
        pages_count = get_pages_count(html)
        for page in range(1, pages_count + 1):
            time.sleep(random.randint(2, 6))
            print(f"Парсинг страницы {page} из {pages_count}...")
            html = get_html(url, params={"page": page})
            get_python_kinopoisk(html, page)
    print(movie)

    # get_python_kinopoisk(html)
    with open("python-org-kinopoisk_test.html", "w", encoding="utf8") as f:
        f.write(html)
