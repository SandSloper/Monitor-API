from flask import Blueprint, url_for

start = Blueprint("start", __name__, static_url_path='static', static_folder='static',template_folder='templates')

from . import route