from back_end.converters import *
from flask import Flask, render_template, json, request

app = Flask(__name__)
app.secret_key = "supersecret"


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/update-units", methods=["POST"])
def update_units():
    print("Incoming...")
    unit = request.get_json()["unit_type"]
    if unit == "CURR":
        converter = Currency()
        return json.dumps({"units": converter.get_currencies()}), 200
    else:
        converter = Units()
        return json.dumps({"units": converter.get_units(unit)}), 200


@app.route("/convert", methods=["POST"])
def convert_units():
    print("Incoming...")
    data = request.get_json()
    unit_in = data["unit-in"]
    unit_out = data["unit-out"]
    val = float(data["val"])
    unit_type = data["unit-type"]
    converted = None
    if unit_type == "CURR":
        c = Currency()
        converted = c.convert(unit_in, unit_out, val)
    else:
        u = Units()
        converted = u.convert(unit_type, unit_in, unit_out, val)

    return json.dumps({"converted": converted}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
