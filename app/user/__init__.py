from flask import Blueprint

user = Blueprint("user", __name__,static_folder='static',template_folder='templates')

from . import routes