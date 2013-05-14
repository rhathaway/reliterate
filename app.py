import uuid
from random import randrange
from flask import Flask, session, request, redirect, url_for
import json
app = Flask(__name__)


games = []


class Game:
  MAX_PLAYERS = 2
  def __init__(self):
    self.players = []
    self.score = 0
    self.started = False
    self.ended = False
    self.winner = None
    self.the_last_word = None
  def addPlayer(self, player_id):
    self.players.append(player_id)
    if len(self.players) == Game.MAX_PLAYERS:
      self.turn = randrange(0, Game.MAX_PLAYERS)
      self.started = True
  def isPlayerTurn(self, player_id):
    return self.started and self.players[self.turn] == player_id
  def setWinner(self, player_id):
    self.ended = True
    self.winner = player_id


def getGame(player_id):
  global games
    
  # if player is in a game, return that game
  for game in games:
    if player_id in game.players:
      return game

  # if the player is not in a game, then add them to a game with only one player
  for game in games:
    if len(game.players) < Game.MAX_PLAYERS:
      game.addPlayer(player_id)
      return game

  # if none of the above, create a new game and add them
  game = Game()
  game.addPlayer(player_id)
  games.append(game)
  return game


@app.route("/gamestate")
def gamestate():
  if not 'player_id' in session:
    session['player_id'] = str(uuid.uuid1())
  game = getGame(session['player_id'])
  result = { 'gamestate':game.__dict__, 'you':session['player_id'] }

  return json.dumps(result)

@app.route("/move", methods=['GET', 'POST'])
def move():
  
  game = getGame(session['player_id'])
  if not game.isPlayerTurn(session['player_id']):
    return "It's not your turn.";
  
  new_word = request.form['word']
  if not game.the_last_word or game.the_last_word.lower()[-1] == new_word.lower()[0]:
    game.the_last_word = new_word
  else:
    return "Your word must start with the last letter of your opponent's word."

  if not  game.turn:
    game.turn = 1
  else:
    game.turn = 0

  return "";




app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run(debug=True)
