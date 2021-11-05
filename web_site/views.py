from flask import Blueprint, render_template, request, redirect, url_for, json
from flask_login import login_required, current_user
from . import db
from .menu import menu
from .models import Board, Task

views = Blueprint("views", __name__)


@views.route("/")
def home():
    boards = Board.query.all()
    return render_template("home.html", boards=boards, menu=menu)


@views.route("/add_board", methods=['GET', 'POST'])
@login_required
def add_board():
    if request.method == 'POST':
        name = request.form.get("name")
        board_private = request.form.get("is_private") == ""
        new_board = Board(name=name, author=current_user.id, is_private=board_private)
        db.session.add(new_board)
        db.session.commit()
        return redirect(url_for("views.home"))
    return render_template("add_board.html", menu=menu)


@views.route("/board/<id>", methods=['GET', 'POST'])
@login_required
def view_board(id):
    board = Board.query.filter_by(id=id).first()
    if board:
        can_delete = board.author == current_user.id

    if not board or (board.author != current_user.id and board.is_private):
        return render_template("no_board.html")

    if request.method == "POST":
        if current_user.id == board.author:
            text = request.form.get("text")
            new_task = Task(text=text, author=current_user.id, board_id=id)
            db.session.add(new_task)
            db.session.commit()
    tasks = Task.query.filter_by(board_id=id)
    return render_template("view_board.html", board=board, tasks=tasks, can_delete=can_delete, menu=menu)


@views.route("/my_boards", methods=['GET'])
@login_required
def my_boards():
    boards = Board.query.filter_by(author=current_user.id)
    return render_template("my_boards.html", boards=boards, menu=menu)


@views.route("/delete/board/<id>", methods=['GET'])
@login_required
def delete_board(id):
    board = Board.query.filter_by(id=id).first()
    if not board or board.author != current_user.id:
        return render_template("no_board.html", menu=menu)
    db.session.delete(board)
    db.session.commit()
    return redirect(url_for("views.my_boards"))


@views.route("/delete/task/<id>", methods=['GET'])
@login_required
def delete_task(id):
    task = Task.query.filter_by(id=id).first()
    if not task or task.author != current_user.id:
        return render_template("no_board.html", menu=menu)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("views.view_board", id=task.board_id))


@views.route("/find_board", methods=['GET', 'POST'])
def find_board():
    name = request.form['name']
    query = f'SELECT * FROM board WHERE name == "{name}"'
    result = list(db.engine.execute(query))
    if result:
        path = "views.view_board"
        answer = {"result": '<a href=' + f'{url_for(path, id=result[0][0])}' + '> Найденная доска<a>'}
    else:
        answer = {"result": "Такой доски нет"}

    return json.dumps(answer)