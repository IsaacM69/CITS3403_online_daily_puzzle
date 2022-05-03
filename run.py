from flask import Flask
from flask import request
from flask import url_for
from flask import render_template
import sqlalchemy


app = Flask(__name__)

@app.route("/game")
def game():
    return render_template('base.html')