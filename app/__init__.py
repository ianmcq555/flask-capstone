from flask import Flask
from config import Config
from .auth.routes import auth
from .nutrition.routes import nutrition
from flask_migrate import Migrate
from .models import db, User
from flask_login import LoginManager

app = Flask(__name__)
login = LoginManager()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

app.config.from_object(Config)

app.register_blueprint(auth)
app.register_blueprint(nutrition)

db.init_app(app)
migrate = Migrate(app, db)
login.init_app(app)

login.login_view = 'auth.logMeIn'

from . import routes
from . import models