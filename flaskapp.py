from flask import Flask, request, Response, render_template, url_for, flash, redirect, session
from wtforms import SubmitField, Form, FloatField, validators
import pyrqlite.dbapi2 as dbapi2
import random
import sqlite3
import binascii
from socket import gethostname, gethostbyname, gethostbyaddr
from datetime import datetime

IPAddr = ''
computerchoice = ''
useroption = ''
dollar = 0
image = ''
inputtext = ''


# db
# Connect to the database
connection = dbapi2.connect(
    host='rqlite.rqlite.svc',
    #host='localhost',
    port=80,
)

try:
  with connection.cursor() as cursor:
    cursor.execute("CREATE TABLE IF NOT EXISTS rank(id INTEGER PRIMARY KEY AUTOINCREMENT,username string,userselection STRING NOT NULL,computerselection STRING NOT NULL,score INT NOT NULL,date datetime default current_timestamp)")
finally:
    connection.close()

#@app.route('/', methods=['GET', 'POST']) #this so that both url will work
class EndpointAction(object):
  def __init__(self, action):
      self.action = action
      self.response = Response(status=200, headers={})

  def __call__(self, *args):
      response = self.action()
      if response != None:
        return response
      else:
        return self.response


class FlaskAppWrapper(object):
  def __init__(self, app, **configs):
    self.app = app
    self.configs(**configs)
    
  def configs(self, **configs):
    for config, value in configs:
      self.app.config[config.upper()] = value

  def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None,t_methods=None):
    self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler),methods=t_methods)

  def run(self, **kwargs):
    self.app.run(**kwargs)


flask_app = Flask(__name__, static_url_path='/static')
flask_app.config.from_pyfile('config.py')

app = FlaskAppWrapper(flask_app)

def returning_action():
  print("Returning action")
  return render_template('index.html')

#   # @app.route('/gamepage', methods=['POST'])
def gamecall():
  session['inputtext'] = request.form['playerid']
  print("The playerid is '" + session['inputtext'] + "'")
  flash(session['inputtext'],'inputtext')
  # playerid pass
  try:
    if (session['inputtext'] == "" or session['inputtext'] == "myid1234") and str(session['inputtext']).len() < 8:
      return render_template('index.html');
    else:
      return render_template('gamepage.html', inputtext=session['inputtext']);
  finally:
    connection.close()
  print("Gamepage action")

# @app.route('/comp', methods=['GET', 'POST'])
def comp():
  global cur
  global image
  global useroption
  global connection
  global IPAddr
  global dollar
  global computerchoice
  # initiatlise variables.
  dollar = 0
  useroption = ''
  result = ''   #already assign a variable, else will throw error
  text = ''
  winner = ''
  winners = []
  image = ''
  computerchoice = ''

  current_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

  print("inputtext: ", session['inputtext'])

  # get IP of client user
  IPAddr = gethostbyname(gethostname())
  print(gethostbyaddr(gethostname())[0])

  # seek from input buttons
  #option = request.form.getlist('options')
  #print("-------------------------------")

  # make a list of 3 objects
  computerchoice = random.choice(['Rock', 'Paper', 'Scissors'])

  # select text content
  #text = request.form.get('playerid')
  #print(text)
  if request.method == 'POST':
    if request.form['button1'] == 'Rock':
      useroption = 'Rock'
    
    if(request.form['button1'] == 'Paper'):
      useroption = 'Paper'
    
    if(request.form['button1'] == 'Scissors'):
      useroption = 'Scissors'

    print("user option: ",useroption)
    print("computer choice: ", computerchoice)
    
    txt = session['inputtext']+"-"+IPAddr
    print("txt: ", txt)

    try:
      with connection.cursor() as cursor:
        cursor.execute("select score from rank where username = ? ORDER by date DESC", (txt,))
        ans = cursor.fetchone()
        print(ans)
        if useroption == computerchoice:
          result = "It is tie :-) "
          if ans != None:
            dollar = int(ans[0])
          elif ans == None:
            dollar = 0
          if str(useroption) == 'Scissors':
            image = 'scissors-neutral.png'
          elif str(useroption) == 'Paper':
            image = 'paper-neutral.png'
          else:
            image = 'rock-neutral.png'
        elif useroption == 'Paper' and computerchoice == 'Rock':
          result = "You Win.  Computer chose "+ computerchoice + "  !!!  Try again !" 
          if ans != None:
            dollar = int(ans[0]) + 1
          elif ans == None:
            dollar = dollar + 1
          if str(useroption) == 'Paper':
            image = 'paper-green.png'
        elif useroption == 'Scissors' and computerchoice == 'Paper':
          result = "You Win.  Computer chose "+ computerchoice + "  !!!  Try again !"
          if ans != None:
            dollar = int(ans[0]) + 1
          elif ans == None:
            dollar = dollar + 1
          if str(useroption) == 'Scissors':
            image = 'scissors-green.png'
        elif useroption == 'Rock' and computerchoice == 'Scissors':
          result = "You Win.  Computer chose "+ computerchoice + "  !!!  Try again !"
          if ans != None:
            dollar = int(ans[0]) + 1
          elif ans == None:
            dollar = dollar + 1
          if str(useroption) == 'Rock':
            image = 'rock-green.png'
        else:
          result = "You Lose.  Computer chose "+ computerchoice + "  !!! Try again !"
          if ans != None:
            dollar = int(ans[0]) - 1
          elif ans == None:
            dollar = dollar - 1
          if computerchoice == 'Scissors':
            image = 'scissors-red.png'
          elif computerchoice == 'Paper':
            image = 'paper-red.png'
          else:
            image = 'rock-red.png'
        print("list value: ", ans)
        print("dollar: ", dollar)
        cursor.execute("INSERT INTO rank (username,userselection,computerselection,score,date) VALUES (?,?,?,?,?)", (txt,useroption,computerchoice,dollar,current_date))
    finally:
      connection.close()

    print(result)
    print(dollar)
    print(image)
    flash(result,'info') # **POINT 3**
    flash(dollar,'message') # **POINT 3**
    flash(image,'image')
    flash(session['inputtext'],'inputtext')
    try:
      with connection.cursor() as cur:
        cur.execute("SELECT username FROM rank where score > 4 ORDER BY rank.date DESC")
        winners = cur.fetchall()
            # winners = res.fetchall()
        for winner in winners:
            print(winner)
        if winners != None:
            flash(winners,'winnermessage')
    except binascii.Error as err:
      pass
    finally:
      connection.close()
    
    return redirect('comp') # This will make your code run forever #**4**     

  return render_template('gamepage.html', result=result, dollar=dollar, winners=winners, image=image, inputtext=session['inputtext'])
    


app.add_endpoint(endpoint='/', endpoint_name='index_page', handler=returning_action, t_methods=['GET'])
app.add_endpoint(endpoint='/gamepage', endpoint_name='game_page', handler=gamecall, t_methods=['POST'])
app.add_endpoint(endpoint='/comp', endpoint_name='comp_page', handler=comp, t_methods=['GET','POST'])

# __name__ is the name of the current Python module. 
# The app needs to know where it’s located to set up some paths, and __name__ is a convenient way to tell it that.
if __name__ == "__main__":
  app.run()
