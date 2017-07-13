from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector


app = Flask(__name__)

# mysql = MySQLConnector(app, 'wall')
app.secret_key = "This is a secret"


@app.route('/')
def index():
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
