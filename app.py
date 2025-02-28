from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    todos = db.relationship('Todo', backref='category', lazy=True)

    def __repr__(self):
        return f"Category('{self.name}')"

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.Date, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return f"Todo('{self.content}', '{self.date_created}')"

with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_deadline_str = request.form['deadline']
        task_category_name = request.form['category']

        try:
            task_deadline = datetime.strptime(task_deadline_str, '%Y-%m-%d').date() if task_deadline_str else None
        except ValueError:
            task_deadline = None

        task_category = Category.query.filter_by(name=task_category_name).first()
        if not task_category:
            task_category = Category(name=task_category_name)
            db.session.add(task_category)
            db.session.commit()

        new_task = Todo(content=task_content, deadline=task_deadline, category=task_category)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        categories = Category.query.all()
        def today():
            return date.today()
        return render_template('index.html', tasks=tasks, categories=categories, today=today)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/complete/<int:id>')
def complete(id):
    task_to_complete = Todo.query.get_or_404(id)
    task_to_complete.completed = True
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem completing that task'

@app.route('/incomplete/<int:id>')
def incomplete(id):
    task_to_incomplete = Todo.query.get_or_404(id)
    task_to_incomplete.completed = False
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem uncompleting that task'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=50007)