from flask import Flask
from flask_cors import CORS
from app.config import Config
from flask_sqlalchemy  import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.init_app(app)
CORS(app)

from app.users import users
from app.start import start
from app.flaechenportal import f_portal
from app.email import mail

app.register_blueprint(start,url_prefix='/')
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(f_portal, url_prefix='/fp')
app.register_blueprint(mail,url_prefix="/email")

