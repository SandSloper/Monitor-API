from flask import Blueprint

ogc = Blueprint("ogc", __name__,url_prefix='/monitor-api' ,static_url_path='static', static_folder='static',template_folder='templates')

from . import routes