from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    abort
)
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgres://postgres:jaishree@localhost:5432/todoapp"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)  # links sqlalchemy to our flask app

migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    list_id = db.Column(db.Integer, db.ForeignKey("todolists.id"), nullable=False)

    # If you want some useful debugging statements when we print these objects
    def __repr__(self):
        return f"<todo: {self.id},{self.description}>"


class TodoList(db.Model):
    __tablename__ = "todolists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    todo = db.relationship(
        "Todo", backref="list", lazy=True, cascade="all, delete-orphan"
    )


# db.create_all()
# used to sync our models before we were using migrations. But now we are using migrations,
# so let migrations do the work of creating and modifying our schema


@app.route("/lists/<list_id>/todos/create", methods=["POST"])
def create_todo(list_id):
    """Create a new todo item in the current list
    Arguments:
        list_id {int} -- id of current list
    Raises:
        an: internal server error, 500
    Returns:
        json -- new todo item
    """
    body = {}
    error = False
    try:
        description = request.get_json()["description"]
        todo = Todo(description=description, list_id=list_id)
        db.session.add(todo)
        db.session.commit()
        body["description"] = todo.description
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info)
    finally:
        db.session.close()
    if error:
        # The route handler should return something or raise an intentional exception, in case of error.
        # SO, import abort form flask and call abort(<status-code) abort (500)
        # to raise an HTTP exception for internal server error
        abort(500)
    else:
        return jsonify(body)


@app.route("/todos/<todo_id>/set-completed", methods=["POST"])
def set_completed_todo(todo_id):
    """Change to completed status of todo item
    Arguments:
        todo_id {int} -- id of todo item
    """
    try:
        completed = request.get_json()["completed"]
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for("index"))


@app.route("/lists/<list_id>/list-completed", methods=["POST"])
def todolist_completed(list_id):
    """Change the completed status of whole item,
    all child items' status also changes
    Arguments:
        list_id {int} -- id of list item
    """
    try:
        completed = request.get_json()["completed"]
        todolist = TodoList.query.get(list_id)
        todolist.completed = completed
        todos = todolist.todo
        for todo_item in todos:
            todo_item.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for("index"))


@app.route("/todos/<todo_id>", methods=["DELETE"])
def delete_todo_item(todo_id):
    """Deletes a todo item
    Arguments:
        todo_id {int} -- id of todo item to be deleted
    Returns:
        JSON -- Success value
    """
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({"success": True})


@app.route("/lists/<list_id>", methods=["DELETE"])
def delete_list_item(list_id):
    """Deletes the list item 
    Arguments:
        list_id {int} -- id of list item to be deleted
    Returns:
        JSON -- Success Value
    """
    try:
        todolist = TodoList.query.get(list_id)
        todos = todolist.todo
        for todo_item in todos:
            db.session.delete(todo_item)
        db.session.delete(todolist)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({"success": True})


@app.route("/lists/<list_id>")
def get_list_todos(list_id):
    """Returns all lists items and
    todo items of the list_id
    Arguments:
        list_id {int} -- id of list
    
    Returns:
        int -- list id
        list -- all list items
        activelist -- current list
        list -- list of todo items in current list
    """
    return render_template(
        "index.html",
        listID=list_id,
        lists=TodoList.query.all(),
        activelist=TodoList.query.get(list_id),
        todos=Todo.query.filter_by(list_id=list_id).order_by("id").all(),
    )


@app.route("/lists/create", methods=["POST"])
def create_list():
    """Creates a new list item 
    Raises:
        an: internal server error, 500
    Returns:
        JSON -- new list item
    """
    body = {}
    error = False
    try:
        name = request.get_json()["name"]
        list = TodoList(name=name)
        db.session.add(list)
        db.session.commit()
        body["name"] = list.name
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info)
    finally:
        db.session.close()
    if error:
        # The route handler should return something or raise an intentional exception, in case of error.
        # SO, import abort form flask and call abort(<status-code) abort (500)
        # to raise an HTTP exception for internal server error
        abort(500)
    else:
        return jsonify(body)


@app.route("/")
def index():
    return redirect(url_for("get_list_todos", list_id=1))

