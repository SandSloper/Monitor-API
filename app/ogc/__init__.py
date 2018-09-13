from flask import Blueprint

ogc = Blueprint("ogc", __name__, static_url_path='static', static_folder='static',template_folder='templates')

from . import routes