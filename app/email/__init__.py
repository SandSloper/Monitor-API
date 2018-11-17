from flask import Blueprint

mail = Blueprint("mail", __name__, static_url_path='static', static_folder='static',template_folder='templates')

from . import routes