import uuid
from random import randrange
from flask import Flask, session, request, redirect, url_for
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


@app.route("/", methods=['GET', 'POST'])
def index():
  if not 'player_id' in session:
    session['player_id'] = str(uuid.uuid1())
  game = getGame(session['player_id'])
  if request.method == "GET":
    turn_message = "It is NOT your turn."
    if game.isPlayerTurn(session['player_id']):
      turn_message = "It is your turn."
    started_message = "is not"
    if game.started:
      started_message = "is"
    winner_message = ""
    if game.ended:
      if game.winner == session['player_id']:
        winner_message = "You win."
      else:
        winner_message = "You lose."
      
    
    form = "<form method=POST><input type=submit></form>" if game.isPlayerTurn(session['player_id']) else ""

    return "You are player %s<br>You're in game %s<br>%s<br>The game %s started.<br>%s<br>%s" % (session['player_id'], repr(game), turn_message, started_message, winner_message, form)
  else:
    game.setWinner(session['player_id'])
    return redirect(url_for('index'))



app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run(debug=True)
