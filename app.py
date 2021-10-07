from dotenv import load_dotenv
from flask import Flask, render_template, request

import search


load_dotenv()

app = Flask(__name__)


@app.get('/')
def home():

    phrase = request.args.get('phrase', '')
    tracks = search.search(phrase) if phrase else []

    return render_template('main.html', tracks=tracks, phrase=phrase)
