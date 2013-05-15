import uuid
import os
import json
from random import randrange
from flask import Flask, session, request, redirect, url_for
import json
app = Flask(__name__)

alerts = {}
games = []


class Game(json.JSONEncoder):
  MAX_PLAYERS = 2
  def __init__(self):
    self.players = []
    self.score = 0
    self.started = False
    self.ended = False
    self.winner = None
    self.moves = []
  def opponent(self, player_id):
    if self.players[0] == player_id:
      return self.players[1]
    return self.players[0]
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
  def __repr__(self):
    return json.dumps(self.__dict__)


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


@app.route("/debug")
def debug():
  result = ""
  for game in games:
    result += str(game)
  return result

@app.route("/clear")
def clear_games():
  global games
  games = []
  app.secret_key = os.urandom(32)
  return "games cleared";

@app.route("/leavegame")
def leave_game():
  global games
  '''
  game = getGame(session['player_id'])
  game.players.remove(session['player_id'])
  print "Now there are %d players in the game." % (len(game.players))
  game.moves = []
  session['player_id'] = str(uuid.uuid1())
  if game.players:
    alerts[game.players[0]] = "Your opponent left the game."
  '''
  
  try:
    game = getGame(session['player_id'])
    alerts[game.opponent(session['player_id'])] = "Your opponent left the game."
    games.remove(game)  
  except:
    pass
  return ""

@app.route("/gamestate")
def gamestate():
  if not 'player_id' in session:
    session['player_id'] = str(uuid.uuid1())
  game = getGame(session['player_id'])

  alert = None
  if session['player_id'] in alerts:
    alert = alerts[session['player_id']]
    del alerts[session['player_id']]
  
  result = { 'gamestate':game.__dict__, 'you':session['player_id'], 'alert':alert }

  return json.dumps(result)

@app.route("/move", methods=['GET', 'POST'])
def move():
  
  game = getGame(session['player_id'])
  if not game.isPlayerTurn(session['player_id']):
    return "It's not your turn.";
  
  new_word = request.form['word']
  new_word = new_word.strip()
  if game.moves == [] or game.moves[-1].lower()[-1] == new_word.lower()[0]:
    game.moves.append(new_word)
  else:
    return "Your word must start with the last letter of your opponent's word."

  if not  game.turn:
    game.turn = 1
  else:
    game.turn = 0

  return "";



app.secret_key = os.urandom(32)
#app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
