from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(400), nullable=False)
    priority = db.Column(db.String(30), nullable=False)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id



@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_priority = request.form.get('priority')
        n_task = Todo(content=task_content, priority=task_priority)

        try:
            db.session.add(n_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'an unexpected error has occurred'

    else:
        tasks = Todo.query.order_by(Todo.data_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'an unexpected error has occurred'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_update = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task_update.content = request.form['content']
        task_update.priority = request.form.get('priority')
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'an unexpected error has occurred'
    else:
        return render_template('update.html', task=task_update)

if __name__ == "__main__":
    app.run(debug=True)