from flask import Blueprint, render_template, request, redirect, url_for, json
from flask_login import login_required, current_user
from . import db

views = Blueprint("views", __name__)