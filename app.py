# Async data requests are requests that get sent to the server and back to the client without a page refresh.
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from jinja2 import Template
import sys

app = Flask(__name__)  # __name__ takes name given for file
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgres://postgres:UTData20$@localhost:5432/todoapp"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # db obj that links SQLAlchemy to Flask app

# allows use of Flask database migrate commands to initialize, upgrade and downgrade migrations
migrate = Migrate(app, db) # links up Flask app and SQLAlchemy db instance

# models to create and manage to add app functionality?
class ToDo(db.Model):  # to link to SQLAlchemy, class should inherit from db.model
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    # to give useful debugging statements when objs are printed,
    # we can define __repr__ to return a to do with the id and desc
    def __repr__(self):
        return f"<ToDo {self.id} {self.description}>"

# db.create_all() is no longer needed with migrationsd
# sync up models with db using db.create_all
#db.create_all()  # ensures tables are created for all models declared

# create url and url handler on our server, by defining route that listens to todos/create
@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        # use description to create new todo obj
        todo = ToDo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        # could be useful debugging statement, ->
        print(sys.exc_info()) # but terminal may also raise error for you
    finally:
        db.session.close()
        # we'd now tell the controller what to render to the user, by
        # telling the view to re-direct to the index route & re-show the index pg
    if error:
        abort(400)
    else:
        return jsonify(body) #name of route handler that listens for chnage on the index route

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        todo = ToDo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index')) # command that grabs a fresh list of to do items

# route to listen to homepage
@app.route("/")
def index():
    # render_template method allows you to specify that an HTML file be rendered to the user
    return render_template(
        "index.html",
        data=ToDo.query.order_by('id').all(),  # modifying to replace dummy data with real data
    )  # name of html file matches method name

# @app.route('/create, methods=['POST'])
# def create():
#     value1 = request.form.get('fields')
# How does Flask allow you to use data inside of HTML templates?
# By proccessing those HTML templates with Jinja2
#  Jinja allows thatnon-HTML gets embedded inside of HTML files by,
# processing entire file, with the template strings that were in HTML file,
# and then rendering an HTML to the user
# if __name__ == '__main__':
