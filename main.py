import os
from dotenv import load_dotenv
from flask import Flask
from extensions import db
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taskmanager.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "routes.login"

from flask_login import login_manager as _login_manager
from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import models here so db.create_all() knows what tables to create.
# routes.py also imports models, but Python's import cache means the same
# module object is reused — no double-definition will occur.

from models import User, Project, Task

def create_admin():
    admin_email = os.getenv("ADMIN_EMAIL") or "admin@test.com"
    admin_password = os.getenv("ADMIN_PASSWORD") or "Admin1234"

    existing_admin = User.query.filter_by(email=admin_email).first()
    if existing_admin:
        return

    admin = User(
        name="Admin",
        email=admin_email,
        password=generate_password_hash(admin_password, method="pbkdf2:sha256"),
        role="Admin"
    )
    db.session.add(admin)
    db.session.commit()
    print(f"Created default admin: {admin_email} / {admin_password}")

with app.app_context():
    db.create_all()
    create_admin()


# Register routes blueprint
from routes import routes as routes_blueprint
app.register_blueprint(routes_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
