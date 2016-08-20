from flask import render_template, request, redirect, url_for
from models import Category, Todo, Priority, db
from run import app


@app.route('/')
def index():
    return render_template('login.html', error='error')

# gets the newtodo added and then generate a response to send back to the browser
@app.route('/new-task', methods=['POST', 'GET'])
def new():
    if request.method == 'POST':
        category = Category.query.filter_by(id=request.form['category']).first()
        priority = Priority.query.filter_by(id=request.form['priority']).first()
        todo = Todo(category, Priority, request.form['description'])
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template(
            'new-task.html',
            page='new-task',
            categories=Category.query.all(),
            priorities=Priority.query.all()
        )

#Updates the old list
@app.route('/<int:todo_id>', methods=['GET', 'POST'])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if request.method == 'GET':
        return render_template(
            'new-task.html',
            todo=todo,
            categories=Category.query.all(),
            priorities=Priority.query.all()
       )
    else:
        category = Category.query.filter_by(id=request.form['category']).first()
        priority = Priority.query.filter_by(id=request.form['priority']).first()
        description = request.form['description']
        todo.category = category
        todo.priority = priority
        todo.description = description
        db.session.commit()
        return redirect(url_for('index'))

# used to generate categories and todos that will be displayed at the main page.
@app.route('/')
def list_all():
   return render_template(
       'list.html',
       categories=Category.query.all(),
       todos=Todo.query.join(Priority).order_by(Priority.value.desc())
   )


# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' or request.form['password'] == 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('layout'))
    return render_template('login.html', error=error)