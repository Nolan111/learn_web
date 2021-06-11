from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Index Page"


app.debug = True
app.run()


if __name__ == "__main__":
    app.run()
