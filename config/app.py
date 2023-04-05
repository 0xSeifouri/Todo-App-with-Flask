from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    text = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'Todo({self.id} - {self.title} - {self.date})'


@app.route('/', methods=['GET', 'POST'])
def home_view():
    if request.method == 'GET':
        data = Todo.query.all()
        return render_template('home.html', todos=data)

    if request.method == 'POST':
        title = request.form['title']
        add = Todo(title=title)
        db.session.add(add)
        db.session.commit()
    return redirect('/')


@app.route('/edit/<int:pk>', methods=['GET', 'POST'])
def update_view(pk):
    def update_todo(todo_id, title):
        db.session.query(Todo).filter_by(id=todo_id).update({'title': title})
        db.session.commit()

    if request.method == 'GET':
        return render_template('edit.html')

    if request.method == 'POST':
        update_todo(pk, title=request.form['title'])
    return redirect(url_for('home_view'))


@app.route('/delete/<int:pk>')
def delete_view(pk):
    todo = Todo.query.get(pk)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home_view'))
