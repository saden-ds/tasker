from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)	# app inizialization

app.secret_key = 'qweqeqweqe131qwewehgfgq'	#secret key


@app.context_processor
def set_global_html_variable_values():
    if 'user_id' in session:
        is_signet_in = True
    else:
        is_signet_in = False
    
    return {'is_signet_in': is_signet_in}

@app.route ('/')
def index():
	if 'user_id' not in session:	# checking if user is logged in
		return redirect('/login')

	cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='tasker') # connecting to database
	cursor = cnx.cursor(dictionary=True)	 # creates cursor variable

	query = (															# sends commands to data base
		"select tasks.name as task_name, users.name as user_name, tasks.id, tasks.started_at, tasks.finished_at " # selecting variables from table "tasks" which have according user's id 
		"from tasks "
		"left join users on users.id = tasks.user_id "
		"where users.id = %s"
	)											 #                ^
												 #                |    
	cursor.execute(query, (session['user_id'],)) # executes the query, parameter being "user_id" which in query is "%s" 

	tasks = cursor.fetchall() # ?

	cnx.close() # terminates database

	return render_template('index.html', tasks = tasks, user_name = session['user_name']) # renders the "index.html" markup

@app.route ('/tasks/new')
def task_new():
	if 'user_id' not in session:
		return redirect('/login')

	return render_template('task_form.html', error_message='') 

@app.route ('/tasks/create', methods=['post']) # methods[post] - gives ability to send data to database
def task_create():
	if 'user_id' not in session:
		return redirect('/login')

	name = request.form.get('name');	# requests the task's content string
	
	if name == '':		# checking if the content was even written
		return render_template('task_form.html', error_message = 'No task specified')

	cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='tasker')
	cursor = cnx.cursor()

	query = (
		"insert into tasks "	
		"(name, user_id) "	# fills in "tasks" table's "name" & "user_id" coloumns  with values "name" and "user_id"
		"values (%s, %s)"
	)
	data = (name, session['user_id']) # data stores the values "name" and "user_id"

	cursor.execute(query, data)	# executes the query, parameter being "name" and "user_id"

	id = cursor.lastrowid # variable "id" stores id of last edited row in table "tasks"

	# cnx.commit()

	cursor.close()

	cnx.close()

	return redirect('/') # returns the user back to main page

@app.route ('/tasks/<int:id>/delete')
def task_delete(id):
	if 'user_id' not in session:
		return redirect('/login')

	cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='tasker')
	cursor = cnx.cursor()
	cursor.execute('DELETE FROM tasks WHERE id = ' + str(id)) # executes deletion of task which has the specified id

	cursor.close()
	cnx.close()

	return redirect('/') # returns the user back to main page

@app.route ('/tasks/<int:id>/start')
def task_start(id):
	if 'user_id' not in session:
		return redirect('/login')

	cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='tasker')

	cursor = cnx.cursor()

	query = (
		"UPDATE tasks " 
		"SET tasks.finished_at = now() " # sets "finished at" value to current datetime, when starting another task
		"WHERE tasks.user_id = %s "
		"AND tasks.started_at IS NOT NULL "
		"AND tasks.finished_at IS NULL"
	)
	data = (session['user_id'],) 

	cursor.execute(query, data)
	cursor.close()

	cursor = cnx.cursor()

	query = (
		"UPDATE tasks " # sets "started at" value to current datetime 
		"SET tasks.started_at = now() "
		"WHERE tasks.id = %s "
	)
	data = (id,) # id is stored in tuple "data"

	cursor.execute(query, data)

	action_id = cursor.lastrowid # variable "action_id" stores id of last edited row in table "tasks" 

	cursor.close()
	cnx.close()

	return redirect('/')


@app.route ('/tasks/<int:id>/stop')
def task_stop(id):
	if 'user_id' not in session:
		return redirect('/login')

	cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='tasker')

	cursor = cnx.cursor()

	query = (
		"UPDATE tasks "
		"SET tasks.finished_at = now() " # sets "finished at" value to current datetime 
		"WHERE tasks.id = %s "
	)
	data = (id,)  # id is stored in tuple "data"

	cursor.execute(query, data)

	action_id = cursor.lastrowid # variable "action_id" stores id of last edited row in table "tasks" 

	cursor.close()
	cnx.close()

	return redirect('/')
	
	
@app.route ('/login', methods=['GET', 'POST']) # methods gives ability to both send and recieve data from database
def login():
	error = ''
	user_name_error = ''

	if request.method == 'POST':
		name = request.form.get('name') # requests the login name from user
		password = request.form.get('password') # requests the password from user

		if name == '':			# checks if name field is filled
			error = 'Error, please check'
			user_name_error = 'no name specified'
		elif password == '':	# checks if password field is filled
			error = 'Error, no password specified'

		if error != '':			# if theres a fill-in error:
			return render_template('login.html', error_message = error, user_name_error = user_name_error) # renders "login.html" markup with error message

		cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='tasker')
		cursor = cnx.cursor(dictionary=True)

		cursor.execute('select id, password from users where name = %s', (name,))

		user = cursor.fetchone() # ?
		count = cursor.rowcount # counts rows
		cursor.close()

		cnx.close()

		if count != 1: # checks if inputted username is in database
			error = 'User is not found'	
		elif user['password'] != password: # matched username's matching password in database does not correspond with inputted password:
			error = 'Incorrect password' # output error

		if error != '': # if theres a username-password error:
			return render_template('login.html', error_message = error, user_name_error = user_name_error)  # renders "login.html" markup with error message

		session['user_id'] = user['id'] # if login was successful, assigns session user_id and user_name
		session['user_name'] = name

		return redirect('/') # redirect to main page
	else:
		return render_template('login.html', error_message = error, user_name_error = user_name_error) # renders "login.html" markup with error message

@app.route ('/logout')
def logout():
	session.pop('user_id') # deletes session 
	session.pop('user_name')

	return redirect('/login') # redirects user to /login

@app.route ('/plan')
def plan():
	if 'user_id' not in session:
		return redirect('/login')

	return "sasa"

if __name__ == '__main__':		# checking if programm running on app.py
    app.run(debug=True)			# debugging on/off





'''
@app.route ('/')
def hello():
	return render_template('index.html')



@app.route ('/test')
def test():
	return  '<h1>Test page 2</h1>' + '<a href="/">main page</a>'
'''
