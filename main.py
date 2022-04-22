from back_end.converters import *
from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "supersecret"


@app.route("/")
def index():
    c = Currency("https://v6.exchangerate-api.com/v6/5e3fa81ca1fd4ed734a46127/latest/USD")
    currencies = c.get_currencies()

    return render_template("index.html", currencies=currencies)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
