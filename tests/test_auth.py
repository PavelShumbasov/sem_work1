from .help_functions import *


def test_signup(client):
    rv = register(client, **AUTH_DATA)
    assert b'User created!' in rv.data

    rv = register(client, **AUTH_DATA)
    assert b"Email is already in use." in rv.data

    rv = register(client, AUTH_DATA["name"], AUTH_DATA3["email"], AUTH_DATA3["password1"], AUTH_DATA3["password2"])
    assert "Username is already in use." in rv.data.decode('utf-8')

    rv = register(client, AUTH_DATA2["name"], AUTH_DATA2["email"], AUTH_DATA2["password1"],
                  AUTH_DATA2["password2"] + "qwe")
    assert "Password do not match!" in rv.data.decode('utf-8')

    rv = register(client, AUTH_DATA3["name"][:3], AUTH_DATA3["email"], AUTH_DATA3["password1"], AUTH_DATA3["password2"])
    assert "Username is too short." in rv.data.decode('utf-8')

    rv = register(client, AUTH_DATA2["name"], AUTH_DATA2["email"], AUTH_DATA2["password1"][:3],
                  AUTH_DATA2["password2"][:3])
    assert "Password is too short." in rv.data.decode('utf-8')

    rv = register(client, AUTH_DATA2["name"], AUTH_DATA2["email"][:3], AUTH_DATA2["password1"], AUTH_DATA2["password2"])
    assert 'Email is invalid.' in rv.data.decode('utf-8')


def test_login_logout(client):
    """Make sure login and logout works."""

    rv = register(client, **AUTH_DATA)
    assert b'User created!' in rv.data

    rv = logout(client)
    assert b'You are logged out!' in rv.data

    rv = login(client, AUTH_DATA['email'], AUTH_DATA['password1'])
    assert b'Logged in!' in rv.data

    rv = logout(client)
    assert b'You are logged out!' in rv.data

    rv = login(client, AUTH_DATA['email'], AUTH_DATA['password1'] + '111')
    assert b'Password is incorrect.' in rv.data

    rv = login(client, AUTH_DATA3['email'], AUTH_DATA['password1'])
    assert b'Email does not exist.' in rv.data


def test_edit_profile(client):
    rv = register(client, **AUTH_DATA)
    assert b'User created!' in rv.data

    rv = logout(client)
    assert b'You are logged out!' in rv.data

    rv = register(client, **AUTH_DATA2)
    assert b'User created!' in rv.data

    rv = logout(client)
    assert b'You are logged out!' in rv.data

    rv = login(client, AUTH_DATA['email'], AUTH_DATA['password1'])
    assert b'Logged in!' in rv.data

    rv = edit_profile(client, **AUTH_DATA2)
    assert b"Email is already in use." in rv.data

    rv = edit_profile(client, AUTH_DATA["name"], AUTH_DATA["email"], AUTH_DATA["password1"],
                      AUTH_DATA["password2"] + "qwe")
    assert "Password do not match!" in rv.data.decode('utf-8')

    rv = edit_profile(client, AUTH_DATA["name"][:3], AUTH_DATA["email"], AUTH_DATA["password1"], AUTH_DATA["password2"])
    assert "Username is too short." in rv.data.decode('utf-8')

    rv = edit_profile(client, AUTH_DATA["name"], AUTH_DATA["email"], AUTH_DATA["password1"][:3],
                      AUTH_DATA["password2"][:3])
    assert "Password is too short." in rv.data.decode('utf-8')

    rv = edit_profile(client, AUTH_DATA["name"], AUTH_DATA["email"][:3], AUTH_DATA["password1"], AUTH_DATA["password2"])
    assert 'Email is invalid.' in rv.data.decode('utf-8')

    rv = edit_profile(client, **AUTH_DATA3)
    assert b"User updated!" in rv.data



