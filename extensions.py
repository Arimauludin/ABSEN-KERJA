from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login' # Tetap tentukan view login di sini

# Kita juga akan membuat fungsi untuk menginisialisasi ekstensi ini dengan aplikasi Flask.
def init_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)