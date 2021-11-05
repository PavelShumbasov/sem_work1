import os
import tempfile

import pytest

from app import create_app

AUTH_DATA = {"name": "Pavel",
             "email": "pavelshumbasov2335@gmail.com",
             "password1": "qwerty",
             "password2": "qwerty"}

AUTH_DATA2 = {"name": "Pavel123",
              "email": "shumbasov2335@gmail.com",
              "password1": "qwerty",
              "password2": "qwerty"}

AUTH_DATA3 = {"name": "Pavel111",
              "email": "PAshumbasov2335@gmail.com",
              "password1": "qwerty",
              "password2": "qwerty"}


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    data_for_testing = {'TESTING': True,
                        'DATABASE': db_path}
    app = create_app(data_for_testing)

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(db_path)


def register(client, name, email, password1, password2):
    return client.post('/sign_up', data=dict(
        email=email,
        name=name,
        password1=password1,
        password2=password2
    ), follow_redirects=True)


def login(client, username, password):
    return client.post('/login', data=dict(
        email=username,
        password=password,
        remember=True
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def edit_profile(client, name, email, password1, password2):
    return client.post('/edit_profile', data=dict(
        email=email,
        name=name,
        password1=password1,
        password2=password2
    ), follow_redirects=True)


def add_board(client, name, is_private):
    return client.post("/add_board", data=dict(
        name=name,
        is_private=is_private
    ), follow_redirects=True)


def view_board(client, board_id):
    return client.get(f"/board/{board_id}")


def add_new_task(client, board_id, text):
    return client.post(f"/board/{board_id}", data=dict(
        text=text
    ), follow_redirects=True)


def my_boards(client):
    return client.get(f"/my_boards")


def delete_board(client, board_id):
    return client.get(f"/delete/board/{board_id}", follow_redirects=True)


def delete_task(client, task_id):
    return client.get(f"/delete/task/{task_id}", follow_redirects=True)


def visit_home(client):
    return client.get("/")


def find_board(client, name):
    return client.post("/find_board", data=dict(name=name))
