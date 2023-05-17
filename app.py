from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)

app.secret_key = 'qweqeqweqe131qwewehgfgq'


@app.context_processor
def set_global_html_variable_values():
    if 'user_id' in session:
        is_signet_in = True
        user_name = session['user_name']
    else:
        is_signet_in = False
        user_name = ''
    
    return {'is_signet_in': is_signet_in}

@app.route ('/')
def index():
	if 'user_id' not in session:
		return redirect('/login')

	cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='tasker')
	cursor = cnx.cursor(dictionary=True)

	query = (
		"select tasks.name as task_name, users.name as user_name, tasks.id, tasks.started_at, tasks.finished_at "
		"from tasks "
		"left join users on users.id = tasks.user_id "
		"where users.id = %s"
	)

	cursor.execute(query, (session['user_id'],))

	tasks = cursor.fetchall()

	cnx.close()

	return render_template('index.html', tasks = tasks, user_name = session['user_name'])

@app.route ('/tasks/new')
def task_new():
	if 'user_id' not in session:
		return redirect('/login')

	return render_template('task_form.html', error_message = '') 

@app.route ('/tasks/create', methods=['post'])
def task_create():
	if 'user_id' not in session:
		return redirect('/login')

	name = request.form.get('name');

	if name == '':
		return render_template('task_form.html', error_message = 'No task specified') ######

	cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='tasker')
	cursor = cnx.cursor()

	query = (
		"insert into tasks "
		"(name, user_id) "
		"values (%s, %s)"
	)
	data = (name, session['user_id'])

	cursor.execute(query, data)

	id = cursor.lastrowid

	# cnx.commit()

	cursor.close()

	cnx.close()

	return redirect('/')

@app.route ('/tasks/<int:id>/delete')
def task_delete(id):
	if 'user_id' not in session:
		return redirect('/login')

	cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='tasker')
	cursor = cnx.cursor()
	cursor.execute('DELETE FROM tasks WHERE id = ' + str(id))

	cursor.close()
	cnx.close()

	return redirect('/')

@app.route ('/tasks/<int:id>/start')
def task_start(id):
	if 'user_id' not in session:
		return redirect('/login')

	cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='tasker')

	cursor = cnx.cursor()

	query = (
		"UPDATE tasks "
		"SET tasks.finished_at = now() "
		"WHERE tasks.user_id = %s "
		"AND tasks.started_at IS NOT NULL "
		"AND tasks.finished_at IS NULL"
	)
	data = (session['user_id'],)

	cursor.execute(query, data)
	cursor.close()

	cursor = cnx.cursor()

	query = (
		"UPDATE tasks "
		"SET tasks.started_at = now() "
		"WHERE tasks.id = %s "
	)
	data = (id,)

	cursor.execute(query, data)

	action_id = cursor.lastrowid

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
		"SET tasks.finished_at = now() "
		"WHERE tasks.id = %s "
	)
	data = (id,)

	cursor.execute(query, data)

	action_id = cursor.lastrowid

	cursor.close()
	cnx.close()

	return redirect('/')
	
	
@app.route ('/login', methods=['GET', 'POST'])
def login():
	error = ''
	user_name_error = ''

	if request.method == 'POST':
		name = request.form.get('name')
		password = request.form.get('password')

		if name == '':
			error = 'Error, please check'
			user_name_error = 'no name specified'
		elif password == '':
			error = 'Error, no password specified'

		if error != '':
			return render_template('login.html', error_message = error, user_name_error = user_name_error)

		cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='tasker')
		cursor = cnx.cursor(dictionary=True)

		cursor.execute('select id, password from users where name = %s', (name,))

		user = cursor.fetchone()
		count = cursor.rowcount
		cursor.close()

		cnx.close()

		if count != 1:
			error = 'User is not found'	
		elif user['password'] != password:
			error = 'Incorrect password'

		if error != '':
			return render_template('login.html', error_message = error, user_name_error = user_name_error)

		session['user_id'] = user['id'];
		session['user_name'] = name;

		return redirect('/')
	else:
		return render_template('login.html', error_message = error, user_name_error = user_name_error) 

@app.route ('/logout')
def logout():
	if 'user_id' in session:
		session.pop('user_id')
		session.pop('user_name')

	return redirect('/login')

@app.route ('/pass_change', methods=['GET', 'POST'])
def pass_change():
	error = ''

	if 'user_id' not in session:
		return redirect('/login')

	if request.method == 'POST':
		name = request.form.get('name')
		password = request.form.get('password')
		password_confirm = request.form.get('password_confirm')
		
		if password == '':
			error = 'Error, no password specified'
		elif len(password) < 8:
			error = 'Not enough characters'
		elif password != password_confirm:
			error = 'Passwords didn’t match. Try again.'

		if error != '':
			return render_template('pass_change.html', error_message = error)
		'''
		cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='tasker')
		cursor = cnx.cursor(dictionary=True)

		query = (
				"insert into users "
				"(name, password) "
				"values (%s, %s)"
			)
		'''
	
	else: 
		return render_template('pass_change.html', error_message = error)

@app.route ('/signup', methods=['GET', 'POST'])
def signup():

	error = ''
	user_name_error = ''
	name = ''

	if request.method == 'POST':
		name = request.form.get('name')
		password = request.form.get('password')
		password_confirm = request.form.get('password_confirm')

		if name == '':
			error = 'Error, please check'
		elif password == '':
			error = 'Error, no password specified'
		elif len(password) < 8:
			error = 'Not enough characters'
		elif password != password_confirm:
			error = 'Passwords didn’t match. Try again.'

		if error != '':
			return render_template('signup.html', error_message = error, name = name)

		cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='tasker')
		cursor = cnx.cursor(dictionary=True)

		cursor.execute('select name from users where name = %s', (name,))

		row = cursor.fetchone()

		cursor.close()

		if row and row['name'] == name:
			return render_template('signup.html', error_message = 'User already exists', name = name)
		else:
			cursor = cnx.cursor()

			query = (
				"insert into users "
				"(name, password) "
				"values (%s, %s)"
			)

			data = (name, password)

			cursor.execute(query, data)

			id = cursor.lastrowid

			cursor.close()

			cnx.close()

			session['user_id'] = id;
			session['user_name'] = name;

			return redirect('/')
	else:
		return render_template('signup.html', error_message = error, name = name)

if __name__ == '__main__':
    app.run(debug=True)



