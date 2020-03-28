from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from unittest import TestCase
app = Flask(__name__)

boggle_game = Boggle()

app.config['SECRET_KEY'] = 'agooddaytodie@tacobell'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
BOARD = "board"

@app.route('/')
def index():
    board = boggle_game.make_board()
    session[BOARD] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)
    return render_template("index.html",
     board=board,
     highscore=highscore,
     nplays=nplays)


@app.route('/check-word')
def check_word():
    
    word = request.args["word"]
    board = session[BOARD]
    res = boggle_game.check_valid_word(board, word)

    return jsonify({'res': res})

@app.route('/post-score', methods=["POST"])
def post_score():

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session["nplays"] = nplays + 1
    session["highscore"] = max(score, highscore)

    res = score > highscore

    return jsonify({'record': res})
