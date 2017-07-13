from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import md5
app = Flask(__name__)
mysql = MySQLConnector(app,'friendsdb')

@app.route('/')
def index():                          # run query with query_db()
    return render_template('index.html')

@app.route('/log', methods=['POST'])
def create():
    query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (:first_name, :last_name, :occupation, NOW(), NOW())"
    # We'll then create a dictionary of data from the POST data received.
    lastname = md5.new(request.form['last_name']).hexdigest();
    print lastname
    data = {
             'first_name': request.form['first_name'],
             'last_name':  lastname,
             'occupation': request.form['occupation']
           }
    # Run query, with dictionary values injected into the query.
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/friends/<friend_id>')
def show(friend_id):
    # Write query to select specific user by id. At every point where
    # we want to insert data, we write ":" and variable name.
    query = "SELECT * FROM friends WHERE id = :specific_id"
    # Then define a dictionary with key that matches :variable_name in query.
    data = {'specific_id': friend_id}
    # Run query with inserted data.
    friends = mysql.query_db(query, data)
    # Friends should be a list with a single object,
    # so we pass the value at [0] to our template under alias one_friend.
    return render_template('index.html', one_friend=friends[0])

@app.route('/remove_friend/<friend_id>', methods=['POST'])
def delete(friend_id):
    
    query = "DELETE FROM friends WHERE id = :id"
    data = {'id': friend_id}
    mysql.query_db(query, data)
    return redirect('/')

app.run(debug=True)


from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector


app = Flask(__name__)
mysql = MySQLConnector(app, 'wall')
app.secret_key = "This is a secret"


@app.route('/')
def index():
    query = "SELECT * FROM wall"
    wall = mysql.query_db(query)
    print wall
    return render_template("index.html")

@app.route('/register') 
def register():
    return render_template("wall.html")

@app.route('/login') 
def login():
    return render_template("wall.html")

@app.route('/success') 
def success():
    return render_template("wall.html")

@app.route('/logout')
def logOut():
   
    return redirect('index.html')

app.run(debug=True)
