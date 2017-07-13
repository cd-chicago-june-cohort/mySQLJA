from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import md5


app = Flask(__name__)
mysql = MySQLConnector(app, 'wall')
app.secret_key = "This is a secret"


@app.route('/')
def index():

    return render_template("index.html")

@app.route('/register', methods =['POST']) 
def register():
    if request.method=='POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = md5.new(request.form['password']).hexdigest();
        isNewUser = True
        parameters = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password
        }
        look_for_user= 'select * from users where email = :email'
        result={'email':email}
        check = mysql.query_db(look_for_user, result)
        print check
        if len(first_name)< 1:
            flash('name is required')
            isNewUser = False
            return redirect('/')  
        if len(last_name)< 1:
            flash('last name is required')
            isNewUser = False
            return redirect('/')  
        if len(email)< 1:
            flash('email is required')
            isNewUser = False
            return redirect('/')  
        if len(password)< 1:
            flash('password is required')
            isNewUser = False
            return redirect('/')  
        if len(check) == 1:
            isNewUser = False
            flash('email already registered')
            return redirect ('/')
        if request.form['password'] != request.form['password_conf']:
            flash('password does not match')
            return redirect('/')
        else:    
           insert_newUser = 'INSERT INTO users (first_name, last_name, email, password, created_at, uptdated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())'
           mysql.query_db(insert_newUser, parameters)
           return redirect('/success')

@app.route('/login', methods = ['POST']) 
def login():

        email = request.form['email']
        password = md5.new(request.form['password']).hexdigest()
        # isNewUser= True
        user_query = 'SELECT * FROM users WHERE email = :email AND password = :password'
        query_data = {
            'email':request.form['email'],
            'password': md5.new(request.form['password']).hexdigest()
        }
        user_list = mysql.query_db(user_query, query_data)
        # if len(email)< 1:
        #     flash('email is required')
        #     isNewUser = False
        #     return redirect('/')  
        # if len(password)< 1:
        #     flash('password name is required')
        #     isNewUser = False
        #     return redirect('/')
        if user_list == []:
            flash('invalid email or password!')
            return redirect('/')
        session['user_list']= user_list
        return redirect('/success')

@app.route('/success') 
def success():
    return render_template("wall.html")

# @app.route('post_message/<_id>')
# def post_message():
#     return ren


@app.route('/logOut')
def logOut():
    
    return redirect('/')

app.run(debug=True)   