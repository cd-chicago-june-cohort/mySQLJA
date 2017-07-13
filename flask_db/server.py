# importing tools from different libraries
from flask import Flask, session, request, redirect, render_template
# importing the MySQLConnector from the mysqlconnection.py file
from mysqlconnection import MySQLConnector

app = Flask(__name__)                       # instantiating a flask object

mysql = MySQLConnector(app, 'world')        # instantiating a connection to MySQL server

@app.route('/', methods=['POST', 'GET'])    # defining the root route
def index():                                # defining a function
    countries = []                          # creating an empty array

    # create a default query independent of data validation
    sql_query = 'select name, code, population, indep_year from countries'
    sql_parameters ={}
    if request.method == 'POST':            # determine the HTTP method
        # create variables to store the information submitted in the form
        server_population_max = request.form['html_population_max']
        server_independence = request.form['html_independence']

        # begin data validation
        if len(server_independence) > 0 and len(server_population_max) > 0:     # case1: both inputs have been entered
            # create a dictionary to hold the variables that contain form data
            sql_parameters = {'sql_population_max': server_population_max, 'sql_independence': server_independence}
            # create a query that includes placeholders for the form data
            sql_query = 'select name, code, population, indep_year from countries where population < :sql_population_max and indep_year < :sql_independence'
        elif len(server_independence) > 0:                                      # case2: only independence year entered
            # setting sql_parameters equal to the dictionary that holds the country independence year (k/v pair)
            sql_parameters = {'sql_independence': server_independence}
            # setting the query that can accept the independence year parameter
            sql_query = 'select name, code, population, indep_year from countries where indep_year < :sql_independence'
        elif len(server_population_max) > 0:                                    # case3: validating if only population entered
            # setting parameters to accept only the population data input
            sql_parameters = {'sql_population_max': server_population_max}
            # creating a string to query the database that accepts the population parameter
            sql_query = 'select name, code, population, indep_year from countries where population < :sql_population_max'
        
        # getting the data from the database... for the specified query and paramater(s)
        countries = mysql.query_db(sql_query, sql_parameters)
    else:
        # getting the data from the database... without parameters
        countries = mysql.query_db(sql_query)

    
    print countries
    # render the information while passing data
    return render_template('index.html', country_list=countries)

app.run(debug=True)