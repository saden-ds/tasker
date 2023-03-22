from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)

app.secret_key = 'qweqeqweqe131qwewehgfgq'


@app.context_processor
def set_global_html_variable_values():
    if 'user_id' in session:
        is_signet_in = True
    else:
        is_signet_in = False
    
    return {'is_signet_in': is_signet_in}

@app.route ('/')
def index():
	if 'user_id' not in session:
		return redirect('/login')

	cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='tasker')
	cursor = cnx.cursor(dictionary=True)

	query = (
		"select tasks.name as task_name, users.name as user_name, tasks.id "
		"from tasks "
		"left join users on users.id = tasks.user_id "
		"where users.id = %s"
	)

	cursor.execute(query, (session['user_id'],))

	tasks = cursor.fetchall()

	cursor.close()

	cnx.close()

	return render_template('index.html', tasks = tasks, user_name = session['user_name'])

@app.route ('/tasks/new')
def task_new():
	if 'user_id' not in session:
		return redirect('/login')

	return render_template('task_form.html') 

@app.route ('/tasks/create', methods=['post'])
def task_create():
	if 'user_id' not in session:
		return redirect('/login')

	name = request.form.get('name');

	if name == '':
		return 'Error, task name not specified'

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
	session.pop('user_id')
	session.pop('user_name')

	return redirect('/login')





'''
@app.route ('/')
def hello():
	return render_template('index.html')



@app.route ('/test')
def test():
	return  '<h1>Test page 2</h1>' + '<a href="/">main page</a>'
'''