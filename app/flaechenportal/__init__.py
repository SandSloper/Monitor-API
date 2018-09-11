from flask import Blueprint, url_for

f_portal = Blueprint("f_portal", __name__, static_url_path='static', static_folder='static',template_folder='templates')

from . import routes