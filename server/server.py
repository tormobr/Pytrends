import random
from flask import request
import time
import flask
from flask import Flask, render_template, jsonify
from test import get_trend

app = Flask(__name__)

# Recieves current board settup and calculate best move
@app.route('/', methods=["GET", "POST"])
def recv_pos():
    trend = request.args.get("trend")
    key_words = [trend]
    if not trend:
        key_words = ["apple"]

    fig_json = get_trend(key_words=key_words)
    print(type(fig_json))
    
    user = {'firstname': "Mr.", 'lastname': "My Father's Son"}
    return render_template("main.html", user=fig_json)
    #get_trend(key_words=key_words)

if __name__ == "__main__":
    app.run(host="localhost", port="5000", debug=True)

