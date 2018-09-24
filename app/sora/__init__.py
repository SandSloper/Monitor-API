from flask import Blueprint

sora = Blueprint("sora", __name__, static_url_path='static', static_folder='static',template_folder='templates')

from . import routes