from flask import Flask,session
from flask_cors import CORS
from app.config import Config
from flask_sqlalchemy  import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_session import Session

import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(Config)
# set the logger for development
gunicorn_logger = logging.getLogger("gunicorn.error")
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.init_app(app)
CORS(app)
Session(app)

from app.user import user
from app.sora import sora
from app.admin import admin
from app.monitor import monitor

app.register_blueprint(user, url_prefix='/')
app.register_blueprint(sora,url_prefix="/sora")
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(monitor,url_prefix='/monitor')
