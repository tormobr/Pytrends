import random
from flask import request
import time
import flask
from flask import Flask, render_template
from test import get_trend

app = Flask(__name__)

# Recieves current board settup and calculate best move
@app.route('/', methods=["GET", "POST"])
def recv_pos():
    trend = request.args["trend"]
    key_words = [trend]
    if not trend:
        key_words = ["apple"]

    get_trend(key_words=key_words)
    
    return render_template("main.html", image="world.html")
    #get_trend(key_words=key_words)

if __name__ == "__main__":
    app.run(host="localhost", port="5000", debug=True)

