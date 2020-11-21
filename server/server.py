import random
from flask import request
import time
import flask
from flask import Flask, render_template, jsonify
from map_plotter import get_trend
from names import get_names

app = Flask(__name__)

@app.route('/getchart', methods=["POST"])
def ret_chart():
    trend = request.args.get("trend")
    key_words = [trend]
    if not trend:
        key_words = ["apple"]

    fig_json = get_trend(key_words=key_words)
    return fig_json

@app.route('/')
@app.route('/trends', methods=["GET"])
def display_chart():
    print("this happens")
    trend = request.args.get("trend")
    key_words = [trend]
    if not trend:
        trend="apple"
    key_words = [trend]

    norway = get_trend(country="norway", geo="NO", key_words=key_words)
    murica = get_trend(country="usa", geo="US", key_words=key_words)
    world = get_trend(country="world", geo="", key_words=key_words)
    return render_template("trends.html", norway=norway, usa=murica, world=world, trend_name=trend)

@app.route('/names', methods=["GET"])
def display_names():
    print("this happens")
    arg = request.args.get("names")
    print(arg)
    arg = arg.replace(" ", "")
    print(arg)
    if not arg:
        names = ["Petter"]
    else:
        names = arg.split(",")
    names = [s[0].upper() + s[1:] for s in names]
    print(names)
    fig = get_names(names=names)
    return render_template("names.html", fig=fig)

@app.route('/ruter')
def ruter():
    return render_template("ruter.html")

@app.route('/weather')
def yr():
    return render_template("weather.html")


if __name__ == "__main__":
    app.run(host="localhost", port="5000", debug=True)
