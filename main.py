import os
from dotenv import load_dotenv
from flask import Flask
from extensions import db
from flask_login import LoginManager

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taskmanager.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from routes import *

#create db tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)