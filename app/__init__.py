
from flask import Flask
from flask_session import Session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

def create_app(cfgobj):
    app = Flask(__name__)
    app.config.from_object(cfgobj)
    return app

app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)
app.secret_key = b'\x80$\x8ep\x0e\xf9\xee\r\xa2\xe1\xdd\x16\x18\xaf\xd3\x15'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

sess = Session()
sess.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

from app import routes, models

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))
