from .help_functions import *
import json


def test_empty_db(client):
    """ Проверка создания пустой базы данных """
    rv = client.get('/')
    assert b'No boards' in rv.data


def test_add_new_board(client):
    board_name = "board"
    rv = register(client, **AUTH_DATA)
    assert b'User created!' in rv.data

    rv = add_board(client, name=board_name, is_private=None)
    assert board_name in rv.data.decode('utf-8')

    rv = add_board(client, name=board_name + '1', is_private="")
    assert board_name + '1' not in rv.data.decode('utf-8')

    rv = view_board(client, 1)
    assert board_name in rv.data.decode('utf-8')

    rv = view_board(client, 2)
    assert board_name + '1' in rv.data.decode('utf-8')

    rv = view_board(client, 3)
    assert "Доска недоступна" in rv.data.decode('utf-8')

    rv = logout(client)
    assert b'You are logged out!' in rv.data

    rv = register(client, **AUTH_DATA2)
    assert b'User created!' in rv.data

    rv = view_board(client, 2)
    assert "Доска недоступна" in rv.data.decode('utf-8')


def test_add_task(client):
    board_name = "board"
    task_test = "task1"
    rv = register(client, **AUTH_DATA)
    assert b'User created!' in rv.data

    rv = add_board(client, name=board_name, is_private=0)
    assert board_name in rv.data.decode('utf-8')

    rv = add_new_task(client, board_id=1, text=task_test)
    assert task_test in rv.data.decode('utf-8')

    rv = my_boards(client)
    assert board_name in rv.data.decode('utf-8')

    rv = register(client, **AUTH_DATA2)
    assert b'User created!' in rv.data

    rv = view_board(client, 1)
    assert board_name in rv.data.decode('utf-8')

    rv = add_new_task(client, board_id=1, text=task_test + '1')
    assert task_test + '1' not in rv.data.decode('utf-8')


def test_delete_board(client):
    board_name = "my_board35"
    task_test = "task1"
    rv = register(client, **AUTH_DATA)
    assert b'User created!' in rv.data

    rv = add_board(client, name=board_name, is_private=0)
    assert board_name in rv.data.decode('utf-8')

    rv = delete_board(client, 1)
    assert board_name not in rv.data.decode('utf-8')


def test_delete_task(client):
    board_name = "my_board3512"
    task_test = "task1"
    rv = register(client, **AUTH_DATA)
    assert b'User created!' in rv.data

    rv = add_board(client, name=board_name, is_private=0)
    assert board_name in rv.data.decode('utf-8')

    rv = add_new_task(client, board_id=1, text=task_test)
    assert task_test in rv.data.decode('utf-8')

    rv = delete_task(client, 1)
    assert task_test not in rv.data.decode('utf-8')

    rv = add_new_task(client, board_id=1, text=task_test)
    assert task_test in rv.data.decode('utf-8')

    rv = delete_board(client, 1)
    assert board_name not in rv.data.decode('utf-8')
    assert task_test not in rv.data.decode('utf-8')


def test_visit_home(client):
    board_name = "my_board3512"
    task_test = "task1"
    rv = register(client, **AUTH_DATA)
    assert b'User created!' in rv.data

    rv = add_board(client, name=board_name, is_private=0)
    assert board_name in rv.data.decode('utf-8')

    rv = visit_home(client)
    assert board_name in rv.data.decode('utf-8')

    rv = add_board(client, name=board_name + "123", is_private="")
    assert board_name + "123" not in rv.data.decode('utf-8')


def test_find_board(client):
    board_name = "my_board3512"
    task_test = "task1"
    rv = register(client, **AUTH_DATA)
    assert b'User created!' in rv.data

    rv = add_board(client, name=board_name, is_private=0)
    assert board_name in rv.data.decode('utf-8')

    rv = find_board(client, board_name)
    assert "Найденная доска" in json.loads(rv.data.decode('utf-8')).get("result")

    rv = find_board(client, board_name + "1111111")
    assert "Такой доски нет" in json.loads(rv.data.decode('utf-8')).get("result")

    rv = delete_board(client, 1)
    assert board_name not in rv.data.decode('utf-8')

    rv = find_board(client, board_name)
    assert "Такой доски нет" in json.loads(rv.data.decode('utf-8')).get("result")
