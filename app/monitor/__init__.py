from flask import Blueprint

monitor = Blueprint("monitor", __name__,static_folder='static',template_folder='templates')

from . import routes