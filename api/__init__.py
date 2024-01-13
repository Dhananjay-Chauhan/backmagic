from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
import psycopg2
app = Flask(__name__)
CORS(app) 
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5433/backmagic"
app.config['SECRET_KEY'] = "dingdingdingdingding"
db = SQLAlchemy(app)
admin = Admin(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(reg_no):
    return Admins.query.get(str(reg_no))

from .models import *
from .endpoints import *

@app.before_request
def handle_before_request():
    if not current_user.is_authenticated and request.endpoint and request.endpoint.split('.')[0] == "admin":
        return redirect(url_for("login"))


with app.app_context():
    db.create_all()
    
