import warnings
from boggle.boggle import Boggle
# this is importing the entire class of Boggle from the file boggle.py 
from flask import Flask, request, render_template,redirect, flash, jsonify, session
from random import randint, choice, sample
from operator import add

app = Flask(__name__)
boggle_game = Boggle()

app.config['SECRET_KEY'] = "iloverollerderby12"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 

try:
    from flask_debugtoolbar import DebugToolbarExtension
    debug = DebugToolbarExtension(app)
except ImportError: 
    warnings.warn('Debuging disabled. Install flask_debugtoolbar to enable')
    pass

    

@app.route('/')
def display_start_page(): 
    """displays the start page"""
    return render_template('start.html')

@app.route('/boggle')
def display_boggle_board(): 
    """displays the Boggle board"""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    number_plays = session.get("number_plays", 0)
    print(board)
    return render_template('board.html', board=board, highscore=highscore, number_plays=number_plays)

@app.route('/check-word')
def check_for_word(): 
    """checks whether word entered is a valid word and if it appears on the board"""
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)
        
    return jsonify({'result': response})
    # note you will have to check for the resason we are jsonifying this 
    # I believe we are setting the key as result to the response so that we can access this in our boggle.py app 
    
@app.route('/end-game', methods=["POST"])
def end_game():
    """ends the game updates the sssion information highscore and number_plays"""
    # import pdb 
    # pdb.set_trace()
    score = request.json["score"]
    # this is in request.json vs request.form because we sent the score via the app.js in the endgame() function to this route 
    highscore = session.get("highscore", 0)
    number_plays = session.get("number_plays", 0)
    session["highscore"] = max(score, highscore)
    session["number_plays"] = number_plays + 1
    return "game over"
    # the reason why we are dealing with number_plays and highscore in this file vs the js file is because we are saving that information in sessions so we can update it and keep a running tally

